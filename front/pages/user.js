import CheckTransaction from "../app/components/ConfirmTransaction";
import React, { useEffect, useTransition } from "react";
import styles from "../styles/User.module.css";
import { getSession, signOut } from "next-auth/react";
import UserData from "../app/components/userData/userData";
import LogoutBtn from "../app/components/logoutBtn/logoutBtn";
import { WalletDisconnectButton } from "@solana/wallet-adapter-react-ui";
import { useWallet } from "@solana/wallet-adapter-react";
require("@solana/wallet-adapter-react-ui/styles.css");

export async function getServerSideProps(context) {
  const session = await getSession(context);
  if (!session) {
    return { redirect: { destination: "/" } };
  }
  return {
    props: { userSession: session },
  };
}

export default function Home({ userSession }) {
  const { publicKey, disconnecting, connected } = useWallet();
  const [isPending, startTransition] = useTransition();

  console.log(userSession);
  useEffect(() => {
    startTransition(() => {
      publicKey && console.log(publicKey.toBase58());
    });
  }, [publicKey]);

  useEffect(() => {
    startTransition(() => {
      disconnecting && signOut();
    });
  }, [disconnecting]);

  useEffect(() => {
    startTransition(() => {
      console.log({ disconnecting });
    });
  }, [disconnecting]);

  if (userSession) {
    return (
      <div className={styles.body}>
        {!isPending && (
          <div className={styles.card}>
            <>
              <UserData />
              <CheckTransaction />
              <div className={styles.buttonsRow}>
                {connected || disconnecting ? (
                  <WalletDisconnectButton />
                ) : (
                  <LogoutBtn />

                )}
              </div>
            </>
          </div>
        )}
      </div>
    );
  }
}
