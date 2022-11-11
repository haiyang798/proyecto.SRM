import requests
import paho.mqtt.client as mqtt
import time
import sys


# 连接成功回调函数
# 参数分别为：调用回调函数的客户端实例，用户私有数据，包含代理回复的标志的字典，连接情况
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


# 订阅主题成功回调函数
def on_subscribe(client, userdata, mid, granted_qos):
    print("消息发送成功")


# 收到订阅主题数据回调函数
def on_message(client, userdata, msg):
    print("主题:", msg.topic, " 消息:")
    print(str(msg.payload.decode('utf-8')))


# 获取天气信息
def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather?q=%s&appid=2a08bb06521eab7145f820efb2fd232f" % city
    r = requests.get(url)
    data = r.json()
    weather = data['weather'][0]
    main = data['main']
    wind = data['wind']
    str = "{name} Weather: {description},Temperature: {temp_min}°-{temp_max}, " \
          "Now: {temp}°, the body is feels_like: {feels_like}°, the wind force: level {speed}, the air pressure: " \
          "{pressure} Pa, the humidity: {humidity}%, the sea_level: {sea_level}m, the grnd_level: {grnd_level}m." \
        .format(name=data['name'], description=weather['description'], temp_max=int(float(main['temp_max']) - 273.15), temp_min=
    int(float(main['temp_min']) - 273.15), temp=int(float(main['temp']) - 273.15),
                feels_like=int(float(main['feels_like']) - 273.15),
                speed=wind['speed'], pressure=main['pressure'], humidity=main['humidity'], sea_level=main['sea_level'],
                grnd_level=main['grnd_level'])

    return str


if __name__ == '__main__':
    client = mqtt.Client(protocol=3)
    client.username_pw_set("admin", "123456")
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.connect(host="127.0.0.1", port=1883, keepalive=60)  # 订阅频道2222
    time.sleep(1)
    i = 0
    while True:
        try:
            # 发布MQTT信息
            sensor_data = get_weather('Valencia')
            client.publish(topic="Forecast", payload=sensor_data, qos=1)
            time.sleep(5)
            i += 1
            print('run for %d' % i)
        except KeyboardInterrupt:
            print("EXIT")
            client.disconnect()
            sys.exit(0)
