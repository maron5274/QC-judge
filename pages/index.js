import Head from 'next/head'
import { useState } from 'react'
import axios from 'axios';
import 'antd/dist/antd.css'
import { Table } from 'antd';
import styles from '../styles/Home.module.css'

export default function Home() {
  const [files, setFiles] = useState([]);
  const [tableData, setTableData] = useState([]);
  const [tableData2, setTableData2] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');
  const [numA, setNumA] = useState('');
  const [numB, setNumB] = useState('');
  const [numC, setNumC] = useState('');
  const [numError, setNumError] = useState('');

  const sendFile = async () => {
    if (files.length === 0) {
      setErrorMessage('Select data')
    } else {
      setErrorMessage('')
      let formData = new FormData();
      for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
      }
      const res = await axios.post('http://localhost:8000/file', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log(res);

      const data = [];
      data.push({ key: 0, samplename: 'TierA', value: '', aico: '' });
      res.data[0].map((list) => {
        data.push({ key: 0, samplename: list[0], value: list[1], aico: list[2] });
      });
      data.push({ key: 0, samplename: 'TierB', value: '', aico: '' });
      res.data[1].map((list) => {
        data.push({ key: 0, samplename: list[0], value: list[1], aico: list[2] });
      });
      data.push({ key: 0, samplename: 'TierC', value: '', aico: '' });
      res.data[2].map((list) => {
        data.push({ key: 0, samplename: list[0], value: list[1], aico: list[2] });
      });
      setTableData(data);
      setNumA(`　TierA> ${res.data[3]} data`)
      setNumB(`　TierB> ${res.data[4]} data`)
      setNumC(`　TierC> ${res.data[5]} data`)
      setNumError(`　Error files> ${res.data[6].length} data`)

      const data2 = [];
      res.data[6].map((list) => {
        data2.push({ key: 0, samplename: list});
      });
      setTableData2(data2);
    }
  }

  const columns = [
    {
      title: 'Sample name',
      dataIndex: 'samplename',
      width: 400,
      render(text, record) {
        return {
          props: {
            style: { background: text == "TierA" || text == "TierB" || text == "TierC" ? "yellow" : "" }
          },
          children: <div>{text}</div>
        };
      }
    },
    {
      title: 'Prediction value',
      dataIndex: 'value',
      width: 150,
      render(text, record) {
        return {
          props: {
            style: { background: text == "" || text == "" || text == "" ? "yellow" : "" }
          },
          children: <div>{text}</div>
        };
      }
    },
    {
      title: 'Lattice constant [Å]',
      dataIndex: 'aico',
      width: 150,
      render(text, record) {
        return {
          props: {
            style: { background: text == "" || text == "" || text == "" ? "yellow" : "" }
          },
          children: <div>{text}</div>
        };
      }
    },
  ];

  const columns2 = [
    {
      title: 'Error files',
      dataIndex: 'samplename',
      width: 200,
    }
  ];

  return (
    <>
      <Head>
        <title>HTPI-iQC</title>
      </Head>

      <main>
        <div className={styles.header}>
          <h1>HTPI-iQC: High-Throughput Phase Identification to detect iQC</h1>
        </div>
        <div className={styles.body}>
          <input
            type="file"
            id="avatarInput"
            onChange={(e) => setFiles(e.target.files)}
            directory=""
            webkitdirectory=""
          />
          <button onClick={sendFile}>upload</button>
          <p style={{ color: 'red' }}>{errorMessage}</p>
          <h2>　Results</h2>
          <div className={styles.tableWrapper}>
            <Table
              columns={columns}
              dataSource={tableData}
              pagination={false}
              scroll={{
                y: 400,
              }}
            />

            <h4>{numA}</h4>
            <h4>{numB}</h4>
            <h4>{numC}</h4>

            <Table
              columns={columns2}
              dataSource={tableData2}
              pagination={false}
              scroll={{
                y: 150,
              }}
            />
            <h4>{numError}</h4>

          </div>
        </div>
      </main>
    </>
  )
}
