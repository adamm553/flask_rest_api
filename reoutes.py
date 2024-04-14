BASE_URL = '/products'

# Basic rules:
#  - Return data in json format instead of html templates
#  - Change db name
#  - In db there will be 3 tables: product, user, category

@app.route(f"{BASE_URL}/", methods = ['GET']) # http://url/products
def get_products():
    devices = DeviceModel.query.all()
    return render_template('index.html', devices = devices)
    # If everything is OK -> status 200
    # If something wrong -> 400
        # If user not authenticated -> 401
        # If something does not exist -> 404
        # Error 500 -> App crashed

@app.reoute(f"{BASE_URL}/<int:id>", methods = ['GET']) # http://url/products/1
def get_product():

@app.route(f"{BASE_URL}/create", methods = ['POST'])
def create():
    # if request.method == "GET":
    #     return render_template('create.html')

    # Extract body from request  -> request.body
    # {name: "name1", ...}

    
    if request.method == "POST":
        device = request.form.getlist('devices')
        devices = ",".join(map(str, device))

        # Add body validation
        # Check if user is authenticated
        product_name = request.form['product_name']
        category = request.form['category']
        producer = request.form['producer']
        description = request.form['description']
        price = request.form['price']
        devices = devices

        devices = DeviceModel(
            product_name=product_name,
            category=category,
            producer=producer,
            description=description,
            price=price

        )
        db.session.add(devices)
        db.session.commit()
        return redirect('/')
    
@app.reoute(f"{BASE_URL}/<int:id>", method = ['PUT']) # http://url/products/1 
def update_procut():
    # get id from url -> request.params
    # 
    

@app.route(f"{BASE_URL}/<int:id>", methods=['DELETE'])
def delete(id):
    devices = DeviceModel.query.filter_by(id=id).first()
    if request.method == "POST":
        if devices:
            db.session.delete(devices)
            db.session.commit()
            return redirect('/')
        return render_template('delete.html')     