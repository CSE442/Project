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

public struct TankData{
	public string keyValue;
	public string jsonString;
	public Vector3 tankPos;
	public Quaternion tankRot;
	//bullets
	public Vector3 turretPos;
	public Quaternion turretRot;
}



public class TankControl : MonoBehaviour
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

	private string getKey(){
	
		string keyValue = null;
		foreach(string key in players.Keys){
			player.keyValue = key.ToString();
			keyValue = key.ToString();
		}

		return keyValue;

	}

	public string getCurrentState(){
		string state = null;
		var infile = JSONNode.Parse (player.jsonString);

		state = (infile["variant"]);

		return state;
	}

	public string getStateID(){
		string uuid = null;
		var infile = JSONNode.Parse (player.jsonString);

		uuid = (infile["uuid"]);

		return uuid;
	}

	/*=================== PLAYER ======================
	 * obtains player information
	 * These functions require keyValue to be passed in, 
	 * you can call getKey() to obtain it
	 */
	public string getPlayerID(string keyValue){
		string uuid = null;
		var infile = JSONNode.Parse (player.jsonString);

		uuid = (infile["players"][keyValue]["uuid"].ToString());
		
		return uuid;
	}
	/*=================== TANK ======================
	 * Obtains tank information 
	 * These functions require keyValue to be passed in, 
	 * you can call getKey() to obtain it
	 */
	public string getTankID(string keyValue){
		string uuid = null;
		var infile = JSONNode.Parse (player.jsonString);

		foreach (string key in players.Keys) {
			uuid = (infile["players"][key]["tank"]["uuid"].ToString());
		}

		return uuid;
	}

	public int getTankHealth (string keyValue){
		int health = 0;
		var infile = JSONNode.Parse (player.jsonString);
		/*
		foreach (string key in players.Keys) {
			health = (infile["players"][key]["tank"]["health"].AsInt);
		}
		*/
		health = infile ["players"] [keyValue] ["tank"] ["health"].AsInt;
		return health;
	}

	/*=================== TURRET ======================
	 * obtains turret uuid
	 * These functions require keyValue to be passed in, 
	 * you can call getKey() to obtain it
	 */
	public string getTurretID(string keyValue){
		string uuid = null;
		var infile = JSONNode.Parse (player.jsonString);

		uuid = (infile["players"][keyValue]["tank"]["turret"]["uuid"].ToString());
		
		return uuid;
	}
	
	public Quaternion getTurretAngle(){
		
		float W = 0, X = 0, Y = 0, Z = 0;
		Quaternion pos;
		
		var infile = JSONNode.Parse (player.jsonString);
		
		W = (infile["players"][player.keyValue]["turret"]["orientation"]["angle"]["a"].AsFloat);
		X = (infile["players"][player.keyValue]["turret"]["orientation"]["angle"]["i"].AsFloat);
		Y = (infile["players"][player.keyValue]["turret"]["orientation"]["angle"]["j"].AsFloat);
		
		Z = (infile["players"][player.keyValue]["turret"]["orientation"]["angle"]["k"].AsFloat);
		
		pos = new Quaternion (W, X, Y, Z);	
		
		// Pos is a Quaternion type
		return pos;
	}

	/*=================== WEAPON ======================
	 * These functions require keyValue to be passed in, 
	 * you can call getKey() to obtain it
	 */
	public string getWeaponID(string keyValue){
		string uuid = null;
		var infile = JSONNode.Parse (player.jsonString);

		uuid = (infile["players"][keyValue]["tank"]["turret"]["weapon"]["uuid"].ToString());

		return uuid;
	}

	// The damage the current turret weapon does. 
	public int getWeaponDamage(string keyValue){
		int damage = 0;
		var infile = JSONNode.Parse (player.jsonString);

		damage = (infile["players"][keyValue]["tank"]["turret"]["weapon"]["damage"].AsInt);
		

		return damage;
	}

	// How much ammo the turret has left
	public int getWeaponAmmo(string keyValue){
		int ammo = 0;
		var infile = JSONNode.Parse (player.jsonString);

		ammo = (infile["players"][keyValue]["tank"]["turret"]["weapon"]["ammo"].AsInt);

		return ammo;
	}

	public string getTurretWeapon(string keyValue){
		string weapon = null;
		var infile = JSONNode.Parse (player.jsonString);

		weapon = (infile["players"][keyValue]["tank"]["turret"]["weapon"]["variant"]);


		return weapon;
	}

	/*
	 * getTankPosition 
	 */
 	public Vector3 getTankPosition(){

		float X = 0.0f, Y = 0.0f, Z = 0.0f;
		Vector3 pos;

		var infile = JSON.Parse (player.jsonString);

		// Extract the (X,Y,Z) as a float and make it a new vector 3. 
		X = (infile["players"][player.keyValue]["tank"]["orientation"]["linear"][0].AsFloat);
		Y = (infile["players"][player.keyValue]["tank"]["orientation"]["linear"][1].AsFloat);
		Z = (infile["players"][player.keyValue]["tank"]["orientation"]["linear"][2].AsFloat);

		pos = new Vector3 (X, Y, Z);
		return pos; 
	}

	// Orientation data for tank
	public Quaternion getTankAngle(){
		
		float W = 0, X = 0, Y = 0, Z = 0;
		Quaternion pos;

		var infile = JSONNode.Parse (player.jsonString);

		// Extract the (W,X,Y,Z) as a vector 4. 
		W = (infile["players"][player.keyValue]["tank"]["orientation"]["angle"]["a"].AsFloat);
		X = (infile["players"][player.keyValue]["tank"]["orientation"]["angle"]["i"].AsFloat);
		Y = (infile["players"][player.keyValue]["tank"]["orientation"]["angle"]["j"].AsFloat);
		Z = (infile["players"][player.keyValue]["tank"]["orientation"]["angle"]["k"].AsFloat);

		pos = new Quaternion (W, X, Y, Z);

		return pos;
	}


	private void moveTank(){

		Tank.transform.position = getTankPosition ();
		print(Tank.transform.position);
		Tank.transform.rotation = getTankAngle ();
		print (Tank.transform.rotation);

		return;
	}

	private void handleTurret(){
		Turret.transform.rotation = getTurretAngle ();
		print (Turret.transform.rotation);
	}

	private void handleShoot(/*bullet list?*/)
	{

	}

	/*
	 * This function should hold all tank updating code.
	 */
	private void updateTanks(){

		//getKey ();
		print (player.keyValue);
		moveTank();

		return;
	}

	//*************
	// On startup
	//*************
	void Start () {
		player = new TankData();
		threadInit = false;	//this flag is for a connected hanger program
		tcpIsPaused = false;
		locked = false;

		IPEndPoint localEndpoint = new IPEndPoint (IPAddress.Parse ("127.0.0.1"), 33333);
		try{
			Socket listener = new Socket (AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
			listener.Bind (localEndpoint);
			listener.Listen (10);
			connection = listener;
			//This thread waits to open a connection to Hanger. Hanger sends the connection request
			connectThread = new System.Threading.Thread(socketAccept);
			connectThread.Start();
			//This thread reads furthur input from the hanger
			readThread = new System.Threading.Thread(readData);
			readThread.Start();
		}catch(Exception e){
			print ("Bad things.");
			Console.WriteLine(e.ToString());
			System.Threading.Thread.Sleep(3000);
		}
	}

	void readData(){
		while (!threadInit) {
			//wait for Hanger connection
		}
		//threadInit = false;
		connectThread.Abort ();;
		while (true) {
			byte[] msg = new byte[1024];
			int length = connection.Receive(msg);

			//read input, then sends data to working method
			//doJson(data);
			if (!tcpIsPaused){
				//if(locked == false){
					/*!!!*!!!!*!!!!*/player.jsonString = Encoding.ASCII.GetString(msg,0,length);
					print(player.jsonString);
					if(player.jsonString == "")
						break;
					var infile = JSONNode.Parse (player.jsonString);

					players = new Dictionary<string, JSONNode>();

					foreach (KeyValuePair<String, JSONNode> pair in infile["players"].AsObject) {
						players.Add (pair.Key, pair.Value);

					//}

					//threadInit = true;
					locked = true;
				}
			}
			//print(data);/
			if(player.jsonString == "")
				break;		//hanger closed. Nothing more to do here
			//************
			// on update
			//************
		}
		print ("Reading thread returned");
	}
	void socketAccept(){
		connection = connection.Accept();	//accept connection from hanger, then return
		threadInit = true;
		print("Connected");
		print ("Startup thread returned");
	}

	void Update(){
		//Tank.transform()

		tcpIsPaused = true;

		if (threadInit) {
			getKey();
			moveTank();
			handleTurret();
			//print("so much poop");
		}
		tcpIsPaused = false;
	}
}
