// импортируем класс Gateway из раннее установленного пакета micromq
const Gateway = require('micromq/gateway');

// создаем экземпляр класса Gateway
const app = new Gateway({
  // названия микросервисов, к которым мы будем обращаться
  microservices: ['nftLicense'],
  // настройки rabbitmq
  rabbit: {
    // ссылка для подключения к rabbitmq (default: amqp://guest:guest@localhost:5672)
    url: process.env.RABBIT_URL,
  },
});

// создаем два эндпоинта /friends & /status на метод GET
app.post(['api/verify_nft'], async (req, res) => {
  // делегируем запрос в микросервис users
  await res.delegate('nftLicense');
});

// начинаем слушать порт
app.listen('8000');