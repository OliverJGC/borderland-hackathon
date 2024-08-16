import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css'
import SVG from './assets/mainSvg';

import Loading from './components/loading';

import Form from 'react-bootstrap/Form';

const DataComponent = () => {
  const [data, setData] = useState([]);

  const [inputValue, setInputValue] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const getData = async () => {
    setLoading(true)
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/data', { comment: inputValue });
      setResult(response.data);
    } catch (error) {
      console.error('Error adding number:', error);
    } finally {
      setLoading(false)
    }
  };

  // const toJSON = (e) => {
  //   setLoading(true)
  //   let xlsx = require('xlsx')
  //   e.preventDefault();
  //   if (e.target.files) {
  //     const reader = new FileReader();
  //     reader.onload = (e) => {
  //       const data = e.target.result;
  //       const workbook = xlsx.read(data, { type: "array" });
  //       const sheetName = workbook.SheetNames[0];
  //       const worksheet = workbook.Sheets[sheetName];
  //       const json = xlsx.utils.sheet_to_json(worksheet);
  //       addNewElements(json);
  //     };
  //     reader.readAsArrayBuffer(e.target.files[0]);
  //   }
  // }

  return (
    <div className='container'>
      <div className='subcontainer'>
        <div className='leftSide'>
          <div className='header'>
            <h1>MOODMINER</h1>
            <h2>Sentiment Analysis</h2>
          </div>

          <input
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            placeholder="Input Text"
          />

          <div className='infoContainer'>
            {!loading && result == null ?
              <div className='result'>
                <div className='image-container'>
                  <img src={require('./assets/ai-icon.png')} />
                </div>
                <h2>Waiting for input</h2>
              </div>
              : loading ?
                <div className='result'>
                  <h2><Loading /></h2>
                </div> :
                <div className='result'>
                  <h2>Positive: {(parseFloat(result.Positive) * 100).toFixed(2)}%</h2>
                  <h2>Negative: {(parseFloat(result.Negative) * 100).toFixed(2)}%</h2>
                  <h2>Neutral: {(parseFloat(result.Neutral) * 100).toFixed(2)}%</h2>
                </div>
            }

            <div className='button'>
              <button onClick={() => { getData() }}>Get Result</button>
            </div>
          </div>

          {/* <div className='options'>
            <Form.Group controlId="formFileSm" className="mb-3">
              <Form.Label>Drag your CSV File.</Form.Label>
              <Form.Control accept=".xls,.xlsx,.ods,.csv"
                type="file"  size="sm" />
            </Form.Group>

            <p>.</p>
            <button>Compare</button>
          </div> */}
        </div>

        <div className='rightSide'>
          <SVG />
        </div>
      </div>


    </div>
  );
};

export default DataComponent;
