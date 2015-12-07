using UnityEngine;
using System.Collections;

public class Startup_Screen : MonoBehaviour {

	public GameObject tank;
	public GameObject turret;
	public GameObject text;
	private float time;
	private float rotateSpeed;
	// Use this for initialization
	void Start () {
		tank.transform.position = new Vector3 (-0.17f,8.71f,-6.7f);
		tank.transform.rotation = Quaternion.Euler (359.95f,277.1f,324.08f);
		time = 0f;
		rotateSpeed = .5f;
	}
	
	// Update is called once per frame
	void Update () {
		tank.transform.position = new Vector3 (-0.17f,8.71f+0.2f*Mathf.Sin (2.1f*time),-6.7f + 0.2f*Mathf.Sin (3.1f*time));
		turret.transform.Rotate (new Vector3(0,rotateSpeed,0));
		if (Random.value < 0.03) {
			rotateSpeed -= 0.2f;
		}
		if (Random.value < 0.03) {
			rotateSpeed += 0.2f;
		}
		if (rotateSpeed > 0.7f)
			rotateSpeed = 0.7f;
		if (rotateSpeed < -0.7f)
			rotateSpeed = -0.7f;
		time += 0.01f;
	}
	void OnDisable(){
		text.SetActive (false);
        tank.transform.GetChild(1).transform.GetChild(1).GetComponent<ParticleSystem>().Clear();
        tank.transform.GetChild(1).transform.GetChild(2).GetComponent<ParticleSystem>().Clear();
    }
}
