import Head from 'next/head'
import { useEffect, useState } from 'react'
import axios from 'axios';
import useWebSocket from 'react-use-websocket';
import 'antd/dist/antd.css'
import { Table } from 'antd';
import { Image } from 'antd';
import { Button, Modal, Space } from 'antd';
import styles from '../styles/Home.module.css'
import RingLoader from "react-spinners/RingLoader"

export default function Home() {
  const [files, setFiles] = useState([]);
  const [tableData, setTableData] = useState([]);
  const [tableData2, setTableData2] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');
  const [numA, setNumA] = useState('');
  const [numB, setNumB] = useState('');
  const [numC, setNumC] = useState('');
  const [numError, setNumError] = useState('');
  const [figSrc, setFigSrc] = useState('error.png');
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [modal2Visible, setModal2Visible] = useState(false);
  const [socketUrl, setSocketUrl] = useState('ws://localhost:8000/0');
  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);
  const [message, setMessage] = useState('');
  const [progress, setProgress] = useState('');
  const showModal = () => {
    setIsModalVisible(true);
  };

  const handleOk = () => {
    setIsModalVisible(false);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  const sendFile = async () => {
    if (files.length === 0) {
      setErrorMessage('Select data')
    } else {
      setErrorMessage('')
      showModal();


      let formData = new FormData();
      for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
      }
      setMessage('uploading...');
      const res = await axios.post('http://localhost:8000/uploadfile', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setSocketUrl('ws://localhost:8000/ws');
      const filenameObject = {
        filenames: res.data
      }
      const filenameJson = JSON.stringify(filenameObject);
      sendMessage(filenameJson);

    }
  }

  useEffect(() => {
    if (lastMessage) {
      if (lastMessage.data.slice(-1) !== "%") {
        let object_ = JSON.parse(lastMessage.data)
        setIsModalVisible(false);
        const data = [];
        data.push({ key: 0, samplename: 'TierA', value: '', aico: '' });
        object_.A.map((list) => {
           data.push({ key: 0, samplename: list[0], value: list[1], aico: list[2] });
         });
         data.push({ key: 0, samplename: 'TierB', value: '', aico: '' });
         object_.B.map((list) => {
           data.push({ key: 0, samplename: list[0], value: list[1], aico: list[2] });
         });
         data.push({ key: 0, samplename: 'TierC', value: '', aico: '' });
         object_.C.map((list) => {
           data.push({ key: 0, samplename: list[0], value: list[1], aico: list[2] });
         });
         setTableData(data);
         setNumA(`　TierA> ${object_.numA} data`)
         setNumB(`　TierB> ${object_.numB} data`)
         setNumC(`　TierC> ${object_.numC} data`)
         setNumError(`　Error files> ${object_.error.length} data`)

         const data2 = [];
         object_.error.map((list) => {
           data2.push({ key: 0, samplename: list });
         });
         setTableData2(data2);
      }
    }
  }, [lastMessage]);

  const drawFig = async (record) => {
    if (record.samplename.indexOf('Tier') !== 0) {
      const res2 = await axios.get(`http://localhost:8000/fig/${record.samplename}`,
        { responseType: 'blob' }
      );
      setFigSrc([URL.createObjectURL(res2.data)])
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
            style: {
              background: text == "TierA" || text == "TierB" || text == "TierC" ? "lightyellow" : "",
              height: text == "TierA" || text == "TierB" || text == "TierC" ? "1px" : "60px"
            }
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
            style: {
              background: text == "" || text == "" || text == "" ? "lightyellow" : "",
              height: text == "" || text == "" || text == "" ? "1px" : "60px"
            }
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
            style: {
              background: text == "" || text == "" || text == "" ? "lightyellow" : "",
              height: text == "" || text == "" || text == "" ? "1px" : "60px"
            }
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

  const getMessage = () => {
    if (lastMessage) {
      if (lastMessage.data.slice(-1) == "%") {
        return lastMessage.data;
      }
    } else {
      return message;
    }
  }

  return (
    <>
      <div className={styles.modal}>
        <Modal
          visible={isModalVisible}
          onOk={handleOk}
          onCancel={handleCancel}
          centered
          width={500}
          okButtonProps={{ disabled: true }}
          cancelButtonProps={{ disabled: true }}
        >
          <h1>Screening Now...</h1>
          <h3>Progress>　{getMessage()}</h3>
          <RingLoader color={"#FFBB7A"} size={80} />
        </Modal>

      </div>

      <Head>
        <title>HTPI-iQCs</title>
      </Head>

      <main>
        <div className={styles.header}>
          <h1>HTPI-iQCs: High-Throughput Phase Identification to detect iQCs</h1>
        </div>

        <div className={styles.body}>
          <input
            type="file"
            id="avatarInput"
            onChange={(e) => setFiles(e.target.files)}
            directory=""
            webkitdirectory=""
          />
          <button onClick={() => {

            sendFile();
          }}>Upload</button>

          <Button type="primary" onClick={() => setModal2Visible(true)}>
            Manual is here.
          </Button>
          <Modal
            title="Manual"
            visible={modal2Visible}
            onOk={() => setModal2Visible(false)}
            onCancel={() => setModal2Visible(false)}
            style={{ top: 40 }}
            width={1000}
            cancelButtonProps={{ disabled: true }}
          >
            <h2>What the service</h2>
            <p>　You can carry out the detection screening for icosahedral quasicrystal (iQC) phases in powder X-ray diffraction (PXRD) patterns
              based on trained machine learning models.</p>
            <h2>How to use</h2>
            <p>　Select the folder containing the PXRD data in "ファイルを選択" and press the "upload" button. ※Screening may take some time.</p>
            <p>　If files in selected folder do not match the folllowing standards, they will not be screened and will be shown in the Table: "Error files".</p>
            <h4>　　Files standards</h4>
            <p>　　・The first column and second columns should be diffraction angle [deg.] and Intensity [a.u.], respectively.</p>
            <p>　　　(It does not matter if there is a third and subsequent row.)</p>
            <p>　　・Diffraction data from 20° ～ 80° must exsit, with their intervals 0.01°.</p>
            <p>　　・Lines with information other than diffraction angle and Intensity must begin with "#" or "*".</p>
          </Modal>

          <p style={{ color: 'red' }}>{errorMessage}</p>


          <h2>　Results</h2>

          <div className={styles.result}>
            <div className={styles.tableWrapper}>
              <Table
                columns={columns}
                dataSource={tableData}
                pagination={false}
                size="middle"
                scroll={{
                  y: 350,
                }}
                onRow={(record, rowIndex) => {
                  return {
                    onClick: event => { drawFig(record) }
                  };
                }}
              />

              <p>{numA},{numB},{numC}</p>

              <Table
                columns={columns2}
                dataSource={tableData2}
                pagination={false}
                size="middle"
                scroll={{
                  y: 150,
                }}
              />
              <p>{numError}</p>
            </div>
            <div className={styles.figure}>
              <h2>XRD Data(Click sample to show)</h2>
              <Image
                width={900}
                height={600}
                src={figSrc}
              />
            </div>
          </div>
        </div>
        <div className={styles.footer}>
          <div className={styles.footerLogo}>
            <p>HTPI-iQCs</p>
          </div>
          <div className={styles.footerContent}>
            <ul>
              <li>Hirotaka Uryu</li>
              <li>1521512@ed.tus.ac.jp</li>
            </ul>
          </div>
        </div>
      </main>
    </>
  )
}
