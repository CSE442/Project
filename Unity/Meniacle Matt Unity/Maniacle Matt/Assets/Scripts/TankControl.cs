using UnityEngine;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using SimpleJSON;
using System.IO;
using System.Collections.Generic;

/*	
 *	Tank Controll.cs
 *	Meniacle Matt and the Angry Avenue 
 *	Written By Jacob Wagner and Matt Winnick
 *	CSE-442 Clear Sunglasses
 */

// TODO: Make a class to hold certain tank information.
// TODO: Make a class to hold certain turret information.

public class TankControl : MonoBehaviour
{
	private Socket serverSocket;
    private Socket activeSocket;
    private string accumulatedMessage;
	private bool gameIsInLobby;
    public GameObject Tank;
    public GameObject Turret;

    void Start()
    {
        print("awaiting connection...");
		this.gameIsInLobby = true;
        IPEndPoint localEndpoint = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 33333);
		this.serverSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
		this.serverSocket.Blocking = false; // for the magic sauce
		this.serverSocket.Bind (localEndpoint);
		this.serverSocket.Listen (10);
        this.accumulatedMessage = "";
    }

    void Update()
    {
        long startTime = DateTime.Now.Millisecond;
		if (this.gameIsInLobby)
        {
            try
            {
                this.activeSocket = this.serverSocket.Accept();
                this.activeSocket.Blocking = false; // more magic sauce
                this.gameIsInLobby = false;
            }
            catch (SocketException e)
            {
                print("still waiting for a connection...");
            }
        }
        else
        {
            uint iterationsPerformed = 0;
            while (activeSocket.Available > 0 && iterationsPerformed < 1)
            {
                iterationsPerformed++;
                byte[] messageBuffer = new byte[4096];
                int messageLength = activeSocket.Receive(messageBuffer);
                int startIndex = 0;
                int chopIndex = 0;
                Debug.Assert(messageLength > 0);
                for (int messageByteIndex = 0; messageByteIndex < messageLength; messageByteIndex++)
                {
                    byte messageByte = messageBuffer[messageByteIndex];
                    if (messageByte == 0x03)
                    {
                        startIndex = chopIndex;
                        chopIndex = messageByteIndex;
                        string messageTail = Encoding.ASCII.GetString(messageBuffer, startIndex, chopIndex - startIndex);
                        string fullMessage = this.accumulatedMessage + messageTail;
                        this.accumulatedMessage = "";
                        JSONNode messageJSON = JSONNode.Parse(fullMessage);
                        State state = State.fromJSON(messageJSON);
                        print(fullMessage);
                        print(state.players.Count);
                        Player player = state.players.Values.GetEnumerator().Current;
                        Tank tank = player.tank;
                        Turret turret = tank.turret;
                        this.Tank.transform.position = tank.orientation.position;
                        this.Tank.transform.rotation = tank.orientation.angle;
                        this.Turret.transform.rotation = turret.relativeOrientation.angle;
                        print("player uuid = " + player.uuid.value);
                        //print (tank.orientation.position);
                        //print (tank.orientation.angle);
                    }
                    else if (messageByte == 0x00)
                    {
                        print("message stream terminated");
                    }
                }
                int chopLength = messageLength - chopIndex;
                Debug.Assert(chopLength >= 0);
                if (chopLength > 0)
                {
                    accumulatedMessage += Encoding.ASCII.GetString(messageBuffer, chopIndex, chopLength);
                }
            }
        }
        long endTime = DateTime.Now.Millisecond;
        long elapsedTime = endTime - startTime;
        print("milliseconds elapsed " + elapsedTime);
    }
}

public struct State
{
    public readonly UUID uuid;
    public readonly Dictionary<UUID, Player> players;
    public readonly Dictionary<UUID, IProjectile> projectiles;
    public static State fromJSON(JSONNode node)
    {
        UUID uuid = UUID.fromString(node["uuid"].Value);
        Dictionary<UUID, Player> players = DictionaryUtil.fromJSON<UUID, Player>(node["players"], UUID.fromString, Player.fromJSON);
        //Dictionary<UUID, IProjectile> projectiles = DictionaryUtil.fromJSON<UUID, IProjectile>(node["projectiles"], UUID.fromString, ProjectileUtility.fromJSON);
		Dictionary<UUID, IProjectile> projectiles = new Dictionary<UUID, IProjectile>();
        return new State(uuid, players, projectiles);
    }
    public static State Empty()
    {
        UUID uuid = new UUID(0);
        Dictionary<UUID, Player> players = new Dictionary<UUID, Player>();
        Dictionary<UUID, IProjectile> projectiles = new Dictionary<UUID, IProjectile>();
        return new State(uuid, players, projectiles);
    }
    public State(UUID uuid, Dictionary<UUID, Player> players, Dictionary<UUID, IProjectile> projectiles)
    {
        this.uuid = uuid;
        this.players = players;
        this.projectiles = projectiles;
    }
}

public struct DictionaryUtil
{
    public static Dictionary<Key, Value> fromJSON<Key, Value>(
        JSONNode node,
        Func<string, Key> convertKey,
        Func<JSONNode, Value> convertValue)
    {
        JSONClass objectView = node.AsObject;
        Dictionary<Key, Value> result = new Dictionary<Key, Value>(objectView.Count);
        foreach (KeyValuePair<string, JSONNode> pair in objectView)
        {
            Key key = convertKey(pair.Key);
            Value value = convertValue(pair.Value);
            result.Add(key, value);
        }
        return result;
    }
}

public struct UUID
{
    public readonly UInt64 value;
    public static UUID fromString(string key)
    {
        return new UUID(UInt64.Parse(key));
    }
    public UUID(UInt64 value)
    {
        this.value = value;
    }
}

public struct Player
{
    public readonly UUID uuid;
    public readonly Tank tank;
    public static Player fromJSON(JSONNode node)
    {
		Console.WriteLine ("reading player " + node);
        UUID uuid = UUID.fromString(node["uuid"]);
        Tank tank = Tank.fromJSON(node["tank"]);
        return new Player(uuid, tank);
    }
    public Player(UUID uuid, Tank tank)
    {
        this.uuid = uuid;
        this.tank = tank;
    }
}

public struct Tank
{
    public readonly UUID uuid;
    public readonly Turret turret;
    public readonly Orientation orientation;
    public static Tank fromJSON(JSONNode node)
    {
		Console.WriteLine ("reading tank " + node);
        UUID uuid = UUID.fromString(node["uuid"]);
        Turret turret = Turret.fromJSON(node["turret"]);
        Orientation orientation = Orientation.fromJSON(node["orientation"]);
        return new Tank(uuid, turret, orientation);
    }
    public Tank(UUID uuid, Turret turret, Orientation orientation)
    {
        this.uuid = uuid;
        this.turret = turret;
        this.orientation = orientation;
    }
}

public struct Turret
{
    public readonly UUID uuid;
    public readonly IWeapon weapon;
    public readonly Orientation relativeOrientation;
    public static Turret fromJSON(JSONNode node)
    {
		Console.WriteLine ("reading turret " + node);
        UUID uuid = UUID.fromString(node["uuid"]);
        IWeapon weapon = WeaponUtility.fromJSON(node["weapon"]);
        Orientation relativeOrientation = Orientation.fromJSON(node["orientation"]);
        return new Turret(uuid, weapon, relativeOrientation);
    }
    public Turret(UUID uuid, IWeapon weapon, Orientation relativeOrientation)
    {
        this.uuid = uuid;
        this.weapon = weapon;
        this.relativeOrientation = relativeOrientation;
    }
}

public struct ProjectileUtility
{
    public static IProjectile fromJSON(JSONNode node)
    {
        switch (node["variant"])
        {
            case "DefaultBullet": return DefaultProjectile.fromJSON(node);
            default: throw new Exception("You fucked up!");
        }
    }
}

public interface IProjectile
{
    Result visit<Result>(IProjectileVisitor<Result> visitor);
}

public interface IProjectileVisitor<Result>
{
    Result visitDefaultProjectile(DefaultProjectile projectile);
}

public struct DefaultProjectile : IProjectile
{
    public readonly UUID uuid;
    public readonly uint damage;
    public readonly Orientation orientation;
    public readonly Orientation orientation_derivative;
    public static DefaultProjectile fromJSON(JSONNode node)
    {
        UUID uuid = UUID.fromString(node["uuid"].Value);
        uint damage = (uint)node["damage"].AsInt;
        Orientation orientation = Orientation.fromJSON(node["orientation"]);
        Orientation orientation_derivative = Orientation.fromJSON(node["orientation_derivative"]);
        return new DefaultProjectile(uuid, damage, orientation, orientation_derivative);
    }
    public DefaultProjectile(UUID uuid, uint damage, Orientation orientation, Orientation orientation_derivative)
    {
        this.uuid = uuid;
        this.damage = damage;
        this.orientation = orientation;
        this.orientation_derivative = orientation_derivative;
    }
    public Result visit<Result>(IProjectileVisitor<Result> visitor)
    {
        return visitor.visitDefaultProjectile(this);
    }
}

public struct WeaponUtility
{
    public static IWeapon fromJSON(JSONNode node)
    {
        switch (node["variant"].Value)
        {
            case "DefaultWeapon": return DefaultWeapon.fromJSON(node);
            default: throw new Exception("You fucked up");
        }
    }
}

public interface IWeapon
{
    Result visit<Result>(IWeaponVisitor<Result> visitor);
}

public interface IWeaponVisitor<Result>
{
    Result visitDefaultWeapon(DefaultWeapon weapon);
}

public struct DefaultWeapon : IWeapon
{
    public readonly UUID uuid;
    public readonly uint ammo;
    public static DefaultWeapon fromJSON(JSONNode node)
    {
        UUID uuid = UUID.fromString(node["uuid"].Value);
        uint ammo = (uint)node["ammo"].AsInt;
        return new DefaultWeapon(uuid, ammo);
    }
    public DefaultWeapon(UUID uuid, uint ammo)
    {
        this.uuid = uuid;
        this.ammo = ammo;
    }
    public Result visit<Result>(IWeaponVisitor<Result> visitor)
    {
        return visitor.visitDefaultWeapon(this);
    }
}

public struct QuaternionUtility
{
    public static Quaternion fromJSON(JSONNode node)
    {
        float w = node["a"].AsFloat;
        float x = node["i"].AsFloat;
        float y = node["j"].AsFloat;
        float z = node["k"].AsFloat;
        return new Quaternion(x, y, z, w);
    }
}

public struct Vector3Utility
{
    public static Vector3 fromJSON(JSONNode node)
    {
        float x = node[0].AsFloat;
        float y = node[1].AsFloat;
        float z = node[2].AsFloat;
        return new Vector3(x, y, z);
    }
}

public struct Orientation
{
    public readonly Quaternion angle;
    public readonly Vector3 position;
    public static Orientation fromJSON(JSONNode node)
    {
        Quaternion angle = QuaternionUtility.fromJSON(node["angular"]);
        Vector3 position = Vector3Utility.fromJSON(node["linear"]);
        return new Orientation(position, angle);
    }
    public Orientation(Vector3 position, Quaternion angle)
    {
        this.position = position;
        this.angle = angle;
    }
}

public struct TankData
{
    public string keyValue;
    public string jsonString;
    public Vector3 tankPos;
    public Quaternion tankRot;
    //bullets
    public Vector3 turretPos;
    public Quaternion turretRot;
}

public class TankControlOld : MonoBehaviour
{

    public GameObject Tank;
    public GameObject Turret;

    public bool locked;

    // structure 
    private TankData player;
    private Vector3 location;
    private Vector4 angle;
    public Dictionary<string, JSONNode> players;

    //===============tcp stuff=========
    private Socket connection;
    System.Threading.Thread readThread;
    System.Threading.Thread connectThread;
    public bool threadInit;
    bool tcpIsPaused;
    //bool active;
    //=================================


    //private string fileLocation = "Assets/Scripts/states.json";		//obtain file Location

    private string getKey()
    {

        string keyValue = null;
        foreach (string key in players.Keys)
        {
            player.keyValue = key.ToString();
            keyValue = key.ToString();
        }

        return keyValue;

    }

    public string getCurrentState()
    {
        string state = null;
        var infile = JSONNode.Parse(player.jsonString);

        state = (infile["variant"]);

        return state;
    }

    public string getStateID()
    {
        string uuid = null;
        var infile = JSONNode.Parse(player.jsonString);

        uuid = (infile["uuid"]);

        return uuid;
    }

    /*=================== PLAYER ======================
	 * obtains player information
	 * These functions require keyValue to be passed in, 
	 * you can call getKey() to obtain it
	 */
    public string getPlayerID(string keyValue)
    {
        string uuid = null;
        var infile = JSONNode.Parse(player.jsonString);

        uuid = (infile["players"][keyValue]["uuid"].ToString());

        return uuid;
    }
    /*=================== TANK ======================
	 * Obtains tank information 
	 * These functions require keyValue to be passed in, 
	 * you can call getKey() to obtain it
	 */
    public string getTankID(string keyValue)
    {
        string uuid = null;
        var infile = JSONNode.Parse(player.jsonString);

        foreach (string key in players.Keys)
        {
            uuid = (infile["players"][key]["tank"]["uuid"].ToString());
        }

        return uuid;
    }

    public int getTankHealth(string keyValue)
    {
        int health = 0;
        var infile = JSONNode.Parse(player.jsonString);
        /*
		foreach (string key in players.Keys) {
			health = (infile["players"][key]["tank"]["health"].AsInt);
		}
		*/
        health = infile["players"][keyValue]["tank"]["health"].AsInt;
        return health;
    }

    /*=================== TURRET ======================
	 * obtains turret uuid
	 * These functions require keyValue to be passed in, 
	 * you can call getKey() to obtain it
	 */
    public string getTurretID(string keyValue)
    {
        string uuid = null;
        var infile = JSONNode.Parse(player.jsonString);

        uuid = (infile["players"][keyValue]["tank"]["turret"]["uuid"].ToString());

        return uuid;
    }

    public Quaternion getTurretAngle()
    {

        float W = 0, X = 0, Y = 0, Z = 0;
        Quaternion pos;

        var infile = JSONNode.Parse(player.jsonString);

        W = (infile["players"][player.keyValue]["tank"]["turret"]["orientation"]["angular"]["a"].AsFloat);
        X = (infile["players"][player.keyValue]["tank"]["turret"]["orientation"]["angular"]["i"].AsFloat);
        Y = (infile["players"][player.keyValue]["tank"]["turret"]["orientation"]["angular"]["j"].AsFloat);

        Z = (infile["players"][player.keyValue]["tank"]["turret"]["orientation"]["angular"]["k"].AsFloat);

        pos = new Quaternion(W, X, Y, Z);

        // Pos is a Quaternion type
        return pos;
    }

    /*=================== WEAPON ======================
	 * These functions require keyValue to be passed in, 
	 * you can call getKey() to obtain it
	 */
    public string getWeaponID(string keyValue)
    {
        string uuid = null;
        var infile = JSONNode.Parse(player.jsonString);

        uuid = (infile["players"][keyValue]["tank"]["turret"]["weapon"]["uuid"].ToString());

        return uuid;
    }

    // The damage the current turret weapon does. 
    public int getWeaponDamage(string keyValue)
    {
        int damage = 0;
        var infile = JSONNode.Parse(player.jsonString);

        damage = (infile["players"][keyValue]["tank"]["turret"]["weapon"]["damage"].AsInt);


        return damage;
    }

    // How much ammo the turret has left
    public int getWeaponAmmo(string keyValue)
    {
        int ammo = 0;
        var infile = JSONNode.Parse(player.jsonString);

        ammo = (infile["players"][keyValue]["tank"]["turret"]["weapon"]["ammo"].AsInt);

        return ammo;
    }

    public string getTurretWeapon(string keyValue)
    {
        string weapon = null;
        var infile = JSONNode.Parse(player.jsonString);

        weapon = (infile["players"][keyValue]["tank"]["turret"]["weapon"]["variant"]);


        return weapon;
    }

    /*
	 * getTankPosition 
	 */
    public Vector3 getTankPosition()
    {

        float X = 0.0f, Y = 0.0f, Z = 0.0f;
        Vector3 pos;

        var infile = JSON.Parse(player.jsonString);

        // Extract the (X,Y,Z) as a float and make it a new vector 3. 
        X = (infile["players"][player.keyValue]["tank"]["orientation"]["linear"][0].AsFloat);
        Y = (infile["players"][player.keyValue]["tank"]["orientation"]["linear"][1].AsFloat);
        Z = (infile["players"][player.keyValue]["tank"]["orientation"]["linear"][2].AsFloat);

        pos = new Vector3(X, Y, Z);
        return pos;
    }

    // Orientation data for tank
    public Quaternion getTankAngle()
    {

        float W = 0, X = 0, Y = 0, Z = 0;
        Quaternion pos;

        var infile = JSONNode.Parse(player.jsonString);

        // Extract the (W,X,Y,Z) as a vector 4. 
        W = (infile["players"][player.keyValue]["tank"]["orientation"]["angle"]["a"].AsFloat);
        X = (infile["players"][player.keyValue]["tank"]["orientation"]["angle"]["i"].AsFloat);
        Y = (infile["players"][player.keyValue]["tank"]["orientation"]["angle"]["j"].AsFloat);
        Z = (infile["players"][player.keyValue]["tank"]["orientation"]["angle"]["k"].AsFloat);

        pos = new Quaternion(W, X, Y, Z);

        return pos;
    }


    private void moveTank()
    {

        Tank.transform.position = getTankPosition();
        //print(Tank.transform.position);
        Tank.transform.rotation = getTankAngle();
        //print (Tank.transform.rotation);

        return;
    }

    private void handleTurret()
    {
        Turret.transform.rotation = getTurretAngle();
        //print (Turret.transform.rotation);
    }

    private void handleShoot(/*bullet list?*/)
    {

    }

    /*
	 * This function should hold all tank updating code.
	 */
    private void updateTanks()
    {

        //getKey ();
        //print (player.keyValue);
        moveTank();

        return;
    }

    //*************
    // On startup
    //*************
    void Start()
    {
        player = new TankData();
        threadInit = false; //this flag is for a connected hanger program
        tcpIsPaused = false;
        locked = false;

        IPEndPoint localEndpoint = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 33333);
        try
        {
            Socket listener = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            listener.Bind(localEndpoint);
            listener.Listen(10);
            connection = listener;
            //This thread waits to open a connection to Hanger. Hanger sends the connection request
            connectThread = new System.Threading.Thread(socketAccept);
            connectThread.Start();
            //This thread reads furthur input from the hanger
            readThread = new System.Threading.Thread(readData);
            readThread.Start();
        }
        catch (Exception e)
        {
            print("Bad things.");
            Console.WriteLine(e.ToString());
            System.Threading.Thread.Sleep(3000);
        }
    }

    void readData()
    {
        while (!threadInit)
        {
            //wait for Hanger connection
        }
        //threadInit = false;
        connectThread.Abort();
        String accumulatedMessage = "";
        String runningMessages = "";
        char[] delimiter = { '\x3' };
        String[] jsons;

        while (true)
        {
            print("While loop");
            byte[] messageBuffer = new byte[1024];
            int messageLength = connection.Receive(messageBuffer);
            if (messageLength > 0)
            {
                runningMessages += Encoding.ASCII.GetString(messageBuffer, 0, messageLength);
                print(runningMessages);
                jsons = runningMessages.Split(delimiter, 2);
                if (jsons.Length > 1)
                {
                    accumulatedMessage = jsons[0];
                    runningMessages = jsons[1];
                }
            }
            /*			String accumulatedMessage = "";
                        byte[] messageBuffer      = new byte[1];
                        while (true) {
                            int messageLength = connection.Receive(messageBuffer);
                            if (messageLength > 0) {
                                if (messageBuffer[0] == 0x03) {
                                    break;
                                }
                                else {
                                    accumulatedMessage += Encoding.ASCII.GetString(messageBuffer, 0, messageLength);
                                }
                            }
                        }
            */
            // byte[] msg = new byte[1024];
            // int length = connection.Receive(msg);

            //read input, then sends data to working method
            //doJson(data);
            if (!tcpIsPaused && accumulatedMessage.Length > 0)
            {
                //if(locked == false){
                /*!!!*!!!!*!!!!*///player.jsonString = Encoding.ASCII.GetString(msg,0,length);
                if (runningMessages.Length < 3 && runningMessages.Contains("\x4"))
                    break;
                player.jsonString = accumulatedMessage;
                //print(player.jsonString);
                var infile = JSONNode.Parse(player.jsonString);

                players = new Dictionary<string, JSONNode>();

                foreach (KeyValuePair<String, JSONNode> pair in infile["players"].AsObject)
                {
                    players.Add(pair.Key, pair.Value);

                    //}

                    //threadInit = true;
                    locked = true;
                }
            }
            //print(data);/
            //print(runningMessages);
            if (runningMessages.Length < 3 && runningMessages.Contains("\x4"))
            {
                print("Connection Closed");
                break;      //hanger closed. Nothing more to do here
            }
            //************
            // on update
            //************
        }
        print("Reading thread returned");
    }

    void socketAccept()
    {
        connection = connection.Accept();   //accept connection from hanger, then return
        threadInit = true;
        print("Connected");
        print("Startup thread returned");
    }

    void Update()
    {
        //Tank.transform()
        print("what the fuck");
        tcpIsPaused = true;

        if (locked)
        {
            getKey();
            moveTank();
            handleTurret();
            //print("so much poop");
        }
        tcpIsPaused = false;
    }
}
