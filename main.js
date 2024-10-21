const sharp = require('sharp');
const { createHash } = require('crypto');
const imageHash = require('image-hash');
const fs = require('fs');

// Generate a hash for an image
const getImageHash = (imagePath) => {
  return new Promise((resolve, reject) => {
    imageHash.hash(imagePath, 16, 'hex', (error, hash) => {
      if (error) reject(error);
      resolve(hash);
    });
  });
};

// Compare images and find duplicates
const findDuplicates = async (imagePaths) => {
  const hashes = new Map();

  for (const imagePath of imagePaths) {
    const hash = await getImageHash(imagePath);
    if (hashes.has(hash)) {
      hashes.get(hash).push(imagePath);
    } else {
      hashes.set(hash, [imagePath]);
    }
  }

  // Print duplicates
  for (const [hash, paths] of hashes.entries()) {
    if (paths.length > 1) {
      console.log(`Duplicate images for hash ${hash}:`);
      paths.forEach((path) => console.log(` - ${path}`));
    }
  }
};

// Example usage
const imageDir = './img';
const imagePaths = fs.readdirSync(imageDir).map(file => `${imageDir}/${file}`);

findDuplicates(imagePaths).catch(console.error);
