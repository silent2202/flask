from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def template_test():
    return render_template(
        'index.html', title="Flask Template Test",
        my_str ="Hello Flask!",
        my_list=[x+1 for x in range(30)]
    )
if __name__ == '__main__':
    app.run(debug=True)