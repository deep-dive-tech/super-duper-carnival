using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LoadData : MonoBehaviour
{
    List<Plot> plots = new List<Plot>();
    public Transform datapoint;
    // Start is called before the first frame update
    void Start()
    {
        TextAsset loggerdata = Resources.Load<TextAsset>("output");

        string[] data = loggerdata.text.Split('\n');

        for (int i = 1; i < data.Length - 1; i++)
        {
            string[] row = data[i].Split(new char[] { ',' });

            Plot p = new Plot();

            int.TryParse(row[0], out p.index);
            float.TryParse(row[1], out p.x);
            float.TryParse(row[2], out p.y);
            float.TryParse(row[3], out p.z);

            plots.Add(p);
        }

        foreach (Plot p in plots)
        {
            //Debug.Log(p[1]);
            Instantiate(datapoint, new Vector3(p.x * 10000f, p.y * 10000f, p.z * 10000f), Quaternion.identity);
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}