/* eslint-disable no-restricted-syntax */

const lineReader = require('line-reader');


const getDataFromFile = async (filepath) => {
  return new Promise((resolve) => {
    const lines = [];
    lineReader.eachLine(filepath, (line, last) => {
      lines.push(line);
      if (last) {
        resolve(lines);
      }
    });
  });
};

const dayOne = (lines) => {
  const neededNumbers = new Set();

  for (const line of lines) {
    const asNumber = parseInt(line, 10);

    if (neededNumbers.has(asNumber)) {
      const result = asNumber * (2020 - asNumber);
      return result;
    }
    neededNumbers.add(2020 - asNumber);
  }
  return null;
};


const main = async () => {
  const lines = await getDataFromFile('./inputs/day01.txt');
  const result = dayOne(lines);
  return result;
};

main().then((result) => console.log(result));
