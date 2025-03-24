# 🤖 Control de Gastos Bot

Este bot de Telegram te permite **registrar y controlar tus gastos personales** directamente desde una conversación en Telegram. Guarda tus gastos por categoría, método de pago, descripción y fecha. También puedes establecer un presupuesto mensual y recibir alertas si lo superas.

## 🚀 Características

- Registro guiado con botones (categoría y método de pago)
- Presupuesto mensual por usuario
- Alertas si superas el 80% o 100% del presupuesto
- Consulta de gastos por mes o categoría
- Multiusuario (cada usuario guarda sus datos por separado)
- Datos almacenados en archivos `.csv` y `.txt`
- Interfaz vía Telegram, sin apps externas

---

## 🛠️ Requisitos

- Python 3.8 o superior
- Una cuenta de Telegram
- Un bot creado en @BotFather
- `ngrok` para exposición del webhook (si corres el bot localmente)

---

## ⚙️ Instalación

```bash
git clone https://github.com/miriambc33/controlGastos_bot.git
cd controlGastos_bot
python -m venv venv
venv\Scripts\activate        # En Windows
pip install -r requirements.txt
```

---

## 🔐 Configuración

Crea un archivo `.env` en la raíz con el siguiente contenido:

```env
TOKEN=TU_TOKEN_DE_TELEGRAM
NGROK_URL=https://tu_ngrok_url.ngrok.io
```

> ⚠️ No compartas nunca este archivo. Está oculto en `.gitignore`.

---

## 🟢 Uso

1. Lanza ngrok:

```bash
ngrok http 8443
```

2. Ejecuta el bot:

```bash
python bot.py
```

3. Abre tu bot en Telegram: [https://t.me/controlgastosbot](https://t.me/controlgastosbot)

---

## 📦 Comandos disponibles

| Comando           | Descripción                                      |
|------------------|--------------------------------------------------|
| `/start`          | Bienvenida                                       |
| `/gasto`          | Inicia el registro de un gasto                   |
| `/resumen`        | Muestra todos los gastos registrados             |
| `/resumen_mes`    | Resumen por mes (o `/resumen_mes actual`)        |
| `/gaste_en`       | Consulta por categoría (ej: `/gaste_en comida`)  |
| `/presupuesto`    | Establece un límite mensual                      |
| `/cancelar`       | Cancela el flujo actual                          |

---

## 🧠 Ideas futuras con IA (opcionales)

- Clasificación automática de gastos por IA
- Resúmenes inteligentes con lenguaje natural
- Sugerencias de ahorro personalizadas
- Integración con OpenAI u Ollama

---

## 📝 Licencia

Este proyecto está desarrollado por **Miriam** con fines educativos y personales.
