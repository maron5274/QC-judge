import Head from 'next/head'
import { useState } from 'react'
import axios from 'axios';
import 'antd/dist/antd.css'
import { Table } from 'antd';
import styles from '../styles/Home.module.css'

export default function Home() {
  const [files, setFiles] = useState([]);
  const [tableData, setTableData] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');

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
    }
  }

  const columns = [
    {
      title: 'Samplename',
      dataIndex: 'samplename',
      width: 150,
    },
    {
      title: 'Value',
      dataIndex: 'value',
      width: 150,
    },
    {
      title: 'aico[Å]',
      dataIndex: 'aico',
    },
  ];

  return (
    <>
      <Head>
        <title>high-thoroughput-QC-detection</title>
      </Head>

      <main>
        <div className={styles.header}>
          <h1>HTPI-QC</h1>
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
          <div className={styles.tableWrapper}>
            <Table
              columns={columns}
              dataSource={tableData}
              pagination={false}
              scroll={{
                y: 240,
              }}
            />
          </div>
        </div>
      </main>
    </>
  )
}
