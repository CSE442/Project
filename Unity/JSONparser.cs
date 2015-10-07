using UnityEngine;
using System.Collections;
using SimpleJSON;
using System.IO;

public class JSONparser : MonoBehaviour
{
    private string m_InGameLog = "";
    private Vector2 m_Position = Vector2.zero;

    void P(string aText)
    {
        m_InGameLog += aText + "\n";
    }

    void Test()
    {
        string fileTest = File.ReadAllText("Assets/Scripts/Test.json");
        var inFile = JSONNode.Parse(fileTest);
        P(inFile.ToString(""));
    }

    void Start()
    {
        Test();
        Debug.Log("Results Of Test:\n" + m_InGameLog);
    }

    void OnGUI()
    {
        m_Position = GUILayout.BeginScrollView(m_Position);
        GUILayout.Label(m_InGameLog);
        GUILayout.EndScrollView();
    }

}
