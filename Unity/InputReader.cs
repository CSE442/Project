using UnityEngine;
using System.Collections;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class InputReader : MonoBehaviour {

	private Socket socket;
	System.Threading.Thread newThread;
	System.Threading.Thread openThread;
	bool initialized;
	bool active;

	// Use this for initialization
	void Start () {
		initialized = false;	//this flag is for a connected hanger program
		active = true;			//this flag is used in closing extra threads
		IPEndPoint localEndpoint = new IPEndPoint (IPAddress.Parse ("127.0.0.1"), 33333);
		try{
			Socket listener = new Socket (AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
			listener.Bind (localEndpoint);
			listener.Listen (10);
			socket = listener;
			//This thread waits to open a connection to Hanger. Hanger sends the connection request
			openThread = new System.Threading.Thread(socketAccept);
			openThread.Start();
			//This thread reads furthur input from the hanger
			newThread = new System.Threading.Thread(readData);
			newThread.Start();
		}catch(Exception e){
			Debug.Log ("Bad things.");
			Console.WriteLine(e.ToString());
			System.Threading.Thread.Sleep(3000);
		}
	}
	void readData(){
		while (!initialized) {
			//wait for Hanger connection
		}
		openThread.Abort ();
		while (active) {
			byte[] msg = new byte[1024];
			int length = socket.Receive(msg);
			string data = Encoding.ASCII.GetString(msg,0,length);
			//read input, then sends data to working method
			doJson(data);
			print(data);
			if(data == "")
				break;		//hanger closed. Nothing more to do here
		}
		print ("Reading thread returned");
	}
	void socketAccept(){
		socket = socket.Accept();	//accept connection from hanger, then return
		initialized = true;
		print("Connected");
		print ("Startup thread returned");
	}
	void OnApplicationQuit(){
		initialized = true;			//close the running threads to keep things clean
		active = false;
		newThread.Abort ();
		openThread.Abort ();
		print ("Closed threads");
	}
	void doJson(string data){
		//use the data from hanger

	}
}
