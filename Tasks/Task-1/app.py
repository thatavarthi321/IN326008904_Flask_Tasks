from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():

    name = request.args.get('name')

    if name:

        upper_name = name.upper()
        lower_name = name.lower()
        reverse_name = name[::-1]
        length = len(name)

        return f"""
        <html>
        <body style="background-color:#f0f8ff;
                     font-family:Arial;
                     text-align:center;
                     padding-top:50px;">

            <h1 style="color:blue;">
                HELLO {upper_name} 👋
            </h1>

            <h2>Name Analysis</h2>

            <p><b>Upper Case:</b> {upper_name}</p>
            <p><b>Lower Case:</b> {lower_name}</p>
            <p><b>Reverse Name:</b> {reverse_name}</p>
            <p><b>Character Count:</b> {length}</p>

        </body>
        </html>
        """

    return """
    <h2>Please enter your name in URL</h2>
    <p>Example: ?name=poojitha</p>
    """

if __name__ == '__main__':
    app.run(debug=True)