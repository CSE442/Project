using UnityEngine;
using System;
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


public class TankControl_copy : MonoBehaviour
{

	public GameObject Tank;


	private Vector3 location;
	private Vector4 angle;
	private string file;
	private Dictionary<string, JSONNode> players;
	private Quaternion pastAngle;

	private bool transformBool = false;

	
	private string fileLocation = "Assets/Scripts/states.json";		//obtain file Location

	private string getKey(){
		string keyValue = null;

		foreach(string key in players.Keys){
			keyValue = key.ToString();
		}
		return keyValue;
	}

	public string getCurrentState(){
		string state = null;
		var infile = JSONNode.Parse (file);

		state = (infile["variant"]);

		return state;
	}

	public string getStateID(){
		string uuid = null;
		var infile = JSONNode.Parse (file);

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
		var infile = JSONNode.Parse (file);

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
		var infile = JSONNode.Parse (file);

		foreach (string key in players.Keys) {
			uuid = (infile["players"][key]["tank"]["uuid"].ToString());
		}

		return uuid;
	}

	public int getTankHealth (string keyValue){
		int health = 0;
		var infile = JSONNode.Parse (file);
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
		var infile = JSONNode.Parse (file);

		uuid = (infile["players"][keyValue]["tank"]["turret"]["uuid"].ToString());
		
		return uuid;
	}

	/*=================== WEAPON ======================
	 * These functions require keyValue to be passed in, 
	 * you can call getKey() to obtain it
	 */
	public string getWeaponID(string keyValue){
		string uuid = null;
		var infile = JSONNode.Parse (file);

		uuid = (infile["players"][keyValue]["tank"]["turret"]["weapon"]["uuid"].ToString());

		return uuid;
	}

	// The damage the current turret weapon does. 
	public int getWeaponDamage(string keyValue){
		int damage = 0;
		var infile = JSONNode.Parse (file);

		damage = (infile["players"][keyValue]["tank"]["turret"]["weapon"]["damage"].AsInt);
		

		return damage;
	}

	// How much ammo the turret has left
	public int getWeaponAmmo(string keyValue){
		int ammo = 0;
		var infile = JSONNode.Parse (file);

		ammo = (infile["players"][keyValue]["tank"]["turret"]["weapon"]["ammo"].AsInt);

		return ammo;
	}

	public string getTurretWeapon(string keyValue){
		string weapon = null;
		var infile = JSONNode.Parse (file);

		weapon = (infile["players"][keyValue]["tank"]["turret"]["weapon"]["variant"]);


		return weapon;
	}

	/*
	 * getTankPosition 
	 */
	public Vector3 getTankPosition(string keyValue){

		float X = 0.0f, Y = 0.0f, Z = 0.0f;
		Vector3 pos;

		var infile = JSONNode.Parse (file);

		X = (infile["players"][keyValue]["tank"]["orientation"]["linear"][0].AsFloat);
		Y = (infile["players"][keyValue]["tank"]["orientation"]["linear"][1].AsFloat);
		Z = (infile["players"][keyValue]["tank"]["orientation"]["linear"][2].AsFloat);

		pos = new Vector3 (X, Y, Z);
		return pos;
	}

	// Orientation data for tank
	public Quaternion getTankAngle(string keyValue){
		
		float W = 0, X = 0, Y = 0, Z = 0;
		Quaternion pos;

		var infile = JSONNode.Parse (file);

		W = (infile["players"][keyValue]["tank"]["orientation"]["angle"]["a"].AsFloat);
		X = (infile["players"][keyValue]["tank"]["orientation"]["angle"]["i"].AsFloat);
		Y = (infile["players"][keyValue]["tank"]["orientation"]["angle"]["j"].AsFloat);
		Z = (infile["players"][keyValue]["tank"]["orientation"]["angle"]["k"].AsFloat);

		pos = new Quaternion (W, X, Y, Z);
		//float angle = Quaternion.Angle (pos, pastAngle);

		//return angle;
		return pos;
	}

	private void moveTank(string keyValue){

		Tank.transform.Translate (getTankPosition (getKey()) * Time.deltaTime);
		print(Tank.transform.position);
	}

	private void handleShoot(/*bullet list?*/)
	{

	}
	//*************
	// On startup
	//*************
	void Start(){
		file = File.ReadAllText(fileLocation);

		var infile = JSONNode.Parse (file);
		/*Dictionary<string,JSONNode>*/ players = new Dictionary<string, JSONNode>();
		foreach (KeyValuePair<String, JSONNode> pair in infile["players"].AsObject) {
			players.Add (pair.Key, pair.Value);
		}

		print (getTankHealth(getKey()));
		pastAngle = new Quaternion (0.0f, 0.0f, 0.0f, 1.0f);

		//transform bool used in update() for debug when usisng 1 file. 
		transformBool = false;

	} 
	//************
	// on update
	//************
	void Update(){
		//Tank.transform()

		moveTank (getKey());

		if (transformBool == false){
			Tank.transform.rotation = Quaternion.Lerp (pastAngle, getTankAngle (getKey()), Time.time * 0.1f);
			transformBool = true;
			print (getTankAngle(getKey()));


		}


	}
}