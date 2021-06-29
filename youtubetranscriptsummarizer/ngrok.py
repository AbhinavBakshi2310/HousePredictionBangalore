from pyngrok import ngrok
ngrok.kill()
ngrok.connect(5000, config_path="C:/Users/91700/.ngrok2/ngrok.yml")
# authtoken: 1u9tYhFHieuiUNtJM8atDgG5Lme_3XDz7gCSfKD3nM2rVapGK