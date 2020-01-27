var crypto = require('crypto');

var key = 'rG0AAEdAObpdJjNldv2xXHq019zYyjEQCQgYpDeLDWVF1JO1va3LwgPwmcx1A1C4HQfjNqbBEFgEiKTG5DMrRlhiLpfHChm6uXe6zcACbEXp5E4M0CPDxlN5H603k4FdNjWEvmZgssVYPlIc59VktH03O0MUr7lb0Rk15MFUsDXyqZ6sZzCOcXQfXowNOLGUSBAJmWPqdmfuHznLNFIEiL7vTuhPgzfwT9BWp9tcaBAFoFBtq6hewdXI6mwo5xSe';
var message = 'testemigrar@gmail.com';

var hash = crypto.createHmac('sha256', key).update(message);

console.log(hash.digest('hex'));