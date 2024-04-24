// подключение express
import express from "express";

import { Metaplex, keypairIdentity } from "@metaplex-foundation/js";
import { Connection, clusterApiUrl, Keypair, PublicKey } from "@solana/web3.js";
// создаем объект приложения
const app = express();
// определяем обработчик для маршрута "/"
app.post("/nftLicense/:publicKey", async function(request, response){
    const publicKey = request.params.publicKey;
    let allNFTs = "";
(async () => {
    const connection = new Connection( 
        "https://solana-api.projectserum.com/", "confirmed");
          const keypair = Keypair.generate();
  const metaplex = new Metaplex(connection);
  metaplex.use(keypairIdentity(keypair));
  const owner = new PublicKey(publicKey);
  allNFTs = await metaplex.nfts().findAllByOwner({
    owner: publicKey
});
  //console.log(allNFTs);
})();
    //const jsonData = JSON.parse(data);
     //const publicKey = jsonData.publicKey;
    
    // отправляем ответ
    response.send("allNFTs");
});
// начинаем прослушивать подключения на 3000 порту
app.listen(8080);