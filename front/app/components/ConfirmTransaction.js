
import React, { useState } from 'react';
import axios from 'axios';
import config from "./loginBtn/walletAdaptor"
const CheckTransaction = () => {
 const [transactionSignature, setTransactionSignature] = useState('');

 const handleSubmit = async () => {
    try {
        console.log(config)
      const response = await axios.post('http://localhost:8000/api/confirm_transaction/',config, {
        transaction_public_key: transactionSignature,
      });
      console.log(response.data);
    } catch (error) {
      console.error('Error checking transaction commitment:', error);
    }
 };

 return (
    <div>
      <input
        type="text"
        placeholder="Enter transaction signature"
        value={transactionSignature}
        onChange={(e) => setTransactionSignature(e.target.value)}
      />
      <button onClick={handleSubmit}>Check Transaction Commitment</button>
    </div>
 );
};

export default CheckTransaction;