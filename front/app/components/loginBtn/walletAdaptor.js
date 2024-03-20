import { useEffect, useState } from "react";
import { useWallet } from "@solana/wallet-adapter-react";
import { WalletMultiButton } from "@solana/wallet-adapter-react-ui";
require("@solana/wallet-adapter-react-ui/styles.css");
import base58 from "bs58";
import { signIn, signOut } from "next-auth/react";
import { useAuthRequestChallengeSolana } from "@moralisweb3/next";
import axios from "axios";

export default function WalletAdaptor() {
  const { publicKey, signMessage, disconnecting, disconnect, connected } =
    useWallet();
  const { requestChallengeAsync, error } = useAuthRequestChallengeSolana();

  const signCustomMessage = async () => {
    const address = publicKey.toBase58();
    console.log(publicKey)
    const { message } = await requestChallengeAsync({
      address,
      network: "devnet",
    });
    const encodedMessage = new TextEncoder().encode(message);
    const signedMessage = await signMessage(encodedMessage, "utf8");
    const signature = base58.encode(signedMessage);

    const response = await axios.post("http://127.0.0.1:8000/api/login/", {"public-key": publicKey, "signature" : signature, "msg": message});
    const token = response["data"]["access"]
    const config = {
     headers: {
         'Content-Type': 'application/json', // Указывает, что тело запроса содержит JSON
        'Accept': 'application/json',
        "Authorization": `Bearer ${token}`
     }
    };
    const response2 = await axios.get("http://127.0.0.1:8000/api/ping/", config)
    const news = await axios.get("http://127.0.0.1:8000/api/modules/", config)
    console.log(news)


    try {
      const { error } = await signIn("credentials", {
        message,
        signature,
        network: "Solana",
        redirect: false,
      });
      if (error) {
        throw new Error(error);
      }
    } catch (e) {
      disconnect();
      console.log(e);
      return;
    }
  };

  useEffect(() => {
    if (error) {
      disconnect();
      console.log(error);
    }
  }, [error]);

  useEffect(() => {
    if (disconnecting) {
      signOut({ redirect: false });
    }
  }, [disconnecting]);

  useEffect(() => {
    connected && signCustomMessage();
  }, [connected]);

  return (
    <>
      <WalletMultiButton />
    </>
  );
}
