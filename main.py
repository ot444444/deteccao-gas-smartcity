from machine import Pin, ADC, PWM
from time import sleep
import dht

sensor_gas = ADC(Pin(34)) ## identifica MQ2
sensor_gas.atten(ADC.ATTN_11DB) ## aumenta a faixa de tensao
sensor_gas.width(ADC.WIDTH_12BIT) ## aumenta os niveis de medicao

sensor_clima = dht.DHT22(Pin(27)) ## identifica o DHT22 

buzzer = PWM(Pin(19), freq=2000, duty=0) ## configura o buzzer com PWM
## altera o pino entre on-off em determinada frequencia

servo = PWM(Pin(18), freq=50, duty=77) ## conexao do servo, em 90 graus

botao = Pin(23, Pin.IN, Pin.PULL_UP) ## conecta o botao

valvula_fechada = False ## variavel bool valvula fechada

adc_alerta_gas = 3830 ## alerta de gas
adc_alerta_critico = 3895 ## alerta critico

while True: 
  soma = 0 ## reinicia a soma

  for contador in range(5): 
    leitura_gas = sensor_gas.read()  ## guarda a leitura

    soma = soma + leitura_gas ## adiciona a leitura na soma 
    sleep(0.2)

  media_gas = soma / 5 ## calc media
  print(f"Media do gas: {media_gas}")

  sensor_clima.measure() ## pede nova medicao 
  temperatura = sensor_clima.temperature() ## guarda a temeperatura
  print(f"Temperatura: {temperatura}°C")

  if temperatura < 0 or temperatura > 60: ## entrada invalida
    estado = "TEMPERATURA FORA DA FAIXA"
  elif media_gas >= adc_alerta_critico: ## alerta critico
    estado = "ALERTA CRÍTICO"
  elif media_gas >= adc_alerta_gas and temperatura >= 34: ## pre critico e temp
    estado = "ALERTA CRÍTICO"
  elif media_gas >= adc_alerta_gas: ## pre critico
    estado = "ALERTA DE GAS"
  else: ## normal
    estado = "NORMAL"

  print(f"Estado: {estado}")

  if estado != "NORMAL":
    valvula_fechada = True ## fecha variavel valvula
  elif botao.value() == 0:
    valvula_fechada = False ## abre variavel valvula

  if valvula_fechada:
    servo.duty(77) ## 90 graus
    print("Valvula: fechada")
  else:
    servo.duty(26) ## 0 graus
    print("Valvula: aberta")
  
  if estado == "NORMAL":
    buzzer.duty(0) ## sem som
  elif estado == "ALERTA DE GAS":
    for i in range(4): ## beep em alarme
        buzzer.duty(512)
        sleep(0.5)
        buzzer.duty(0)
        sleep(0.5)
  else:
    buzzer.duty(512) ## beep continuo

  sleep(0.8)

