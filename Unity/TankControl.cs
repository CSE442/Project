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


public class TankControl : MonoBehaviour
{
	public Vector3 location; 
	public Vector4 angle;
	//Tank object to use transform() with 
	public GameObject Tank;
	//public string playerNumber = "player1";
	
	private string fileLocation = "Assets/Scripts/states.json";		//obtain file Location


	public string getCurrentState(string file, Dictionary<string, JSONNode> players){
		string state = null;
		var infile = JSONNode.Parse (file);

		state = (infile["variant"]);

		return state;
	}

	public string getStateID(string file, Dictionary<string, JSONNode> players){
		string uuid = null;
		var infile = JSONNode.Parse (file);

		uuid = (infile["uuid"]);

		return uuid;
	}

	//=================== PLAYER ======================
	//obtains player information
	public string getPlayerID(string file, Dictionary<string,JSONNode> players){
		string uuid = null;
		var infile = JSONNode.Parse (file);

		foreach (string key in players.Keys){
			uuid = (infile["players"][key]["uuid"].ToString());
		}
		return uuid;
	}
	//=================== TANK ======================
	// Obtains tank information 
	public string getTankID(string file, Dictionary<string,JSONNode> players){
		string uuid = null;
		var infile = JSONNode.Parse (file);

		foreach (string key in players.Keys) {
			uuid = (infile["players"][key]["tank"]["uuid"].ToString());
		}

		return uuid;
	}

	public string getTankHealth (string file, Dictionary<string,JSONNode> players){
		string health = null;
		var infile = JSONNode.Parse (file);

		foreach (string key in players.Keys) {
			health = (infile["players"][key]["tank"]["health"].ToString());
		}

		return health;
	}

	//=================== TURRET ======================
	// obtains turret uuid
	public string getTurretID(string file, Dictionary<string,JSONNode> players){
		string uuid = null;
		var infile = JSONNode.Parse (file);
		
		foreach (string key in players.Keys) {
			uuid = (infile["players"][key]["tank"]["turret"]["uuid"].ToString());
		}
		
		return uuid;
	}

	//=================== WEAPON ======================
	public string getWeaponID(string file, Dictionary<string, JSONNode> players){
		string uuid = null;
		var infile = JSONNode.Parse (file);

		foreach (string key in players.Keys) {
			uuid = (infile["players"][key]["tank"]["turret"]["weapon"]["uuid"].ToString());
		}

		return uuid;
	}

	public string getWeaponDamage(string file, Dictionary<string, JSONNode> players){
		string damage = null;
		var infile = JSONNode.Parse (file);
		
		foreach (string key in players.Keys) {
			damage = (infile["players"][key]["tank"]["turret"]["weapon"]["damage"].ToString());
		}

		return damage;
	}

	public string getWeaponAmmo(string file, Dictionary<string, JSONNode> players){
		string ammo = null;
		var infile = JSONNode.Parse (file);
		
		foreach (string key in players.Keys) {
			ammo = (infile["players"][key]["tank"]["turret"]["weapon"]["ammo"].ToString());
		}
		
		return ammo;
	}

	public string getTurretWeapon(string file, Dictionary<string,JSONNode> players ){
		string weapon = null;
		var infile = JSONNode.Parse (file);

		foreach (string key in players.Keys) {
			weapon = (infile["players"][key]["tank"]["turret"]["weapon"]["variant"]);
		}

		return weapon;
	}

	public Vector3 getTankPosition(string file, Dictionary<string, JSONNode> players ){

		// TODO: location transforming

		return location;
	}

	// Orientation data for tank
	public Vector4 getTankAngle(string file){
		
		//TODO: quaternion stuff
		
		return angle;
	}
	// On startup
	void Start(){
		string file = File.ReadAllText(fileLocation);

		var infile = JSONNode.Parse (file);
		Dictionary<string,JSONNode> players = new Dictionary<string, JSONNode>();
		foreach (KeyValuePair<String, JSONNode> pair in infile["players"].AsObject) {
			players.Add (pair.Key, pair.Value);
		}

		print ("Getting player uuid ........");
		print (getPlayerID (file, players));
	
		print ("Getting tank uuid.....");
		print (getTankID (file, players));

		print ("Getting tank health.......");
		print (getTankHealth (file, players));

		print ("Getting turret uuid......");
		print (getTurretID(file, players));

		print ("Getting Tank Weapon......");
		print (getTurretWeapon (file, players));

	} 

	// on update
	void Update(){
		//Tank.transform()
	}
}
