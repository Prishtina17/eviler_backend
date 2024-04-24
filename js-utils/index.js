const { Keypair, Connection } = require('@solana/web3.js');
const { Metaplex,keypairIdentity, bundlrStorage,toMetaplexFile } = require('@metaplex-foundation/js');
const {fs} = require('fs');

async function createMetadata(imageName) {

  // Create an image buffer
  const metadataURI = await metaplex.nfts().uploadMetadata({
    name: "Eviler nft",
    description: "Eviler nft test",

    // Image: await uploadIMG(imageName),
    image: await toMetaplexFile(fs.readFileSync(imageName), "heliusLogo"),
    attributes: [
      { trait_type: "Test", value: "Yes" },
      { trait_type: "Logo", value: "Helius" },
    ],
  });
  return metadataURI;
}

async function createNFT() {
  // Create and upload the metadata
  const metadata = await createMetadata("./heliusLogo.png");
  // Create the NFT
  const nft = await metaplex.nfts().create({
    uri: metadata.uri,
    name: "Helius NFT",
    seller_fee_basis_points: 500, // 5%
    creators: [{ address: wallet.publicKey, verified: true, share: 100 }],
  });

  // Log the NFT mint address
  console.log("NFT:", nft.mintAddress.toBase58());
}
console.log(createMetadata());