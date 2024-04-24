// импортируем класс MicroService из раннее установленного пакета micromq
const MicroMQ = require('micromq');

// создаем экземпляр класса MicroService
const app = new MicroMQ({
  // название микросервиса (оно должно быть таким же, как указано в Gateway)
  name: 'users',
  // настройки rabbitmq
  rabbit: {
    // ссылка для подключения к rabbitmq (default: amqp://guest:guest@localhost:5672)
    url: process.env.RABBIT_URL,
  },
});

// создаем эндпоинт /friends для метода GET
app.get('/friends', (req, res) => {
  // отправляем json ответ
  res.json([
    {
      id: 1,
      name: 'Mikhail Semin',
    },
    {
      id: 2,
      name: 'Ivan Ivanov',
    },
  ]);
});

// создаем эндпоинт /status для метода GET
app.get('/status', (req, res) => {
  // отправляем json ответ
  res.json({
    text: 'Thinking...',
  });
});

// начинаем слушать очередь запросов
app.start();