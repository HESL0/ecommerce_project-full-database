from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import db
from functions import get_all_products, create_product, delete_product
from urllib.parse import parse_qs


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/products":
            connection = db.get_connection()
            products = get_all_products(connection)
            connection.close()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(products).encode("utf-8"))

        elif self.path == "/":
            connection = db.get_connection()
            products = get_all_products(connection)
            connection.close()

            html = """
            <h1>My Store</h1>

            <form method="POST" action="/products">
                <label for="name">Name:</label><br>
                <input type="text" id="name" name="name"><br>

                <label for="price">Price:</label><br>
                <input type="number" id="price" name="price"><br>

                <input type="submit" value="Submit">
            </form>
            """

            for product_id, name, price in products:
                html += f"<p>{name} is {price}$</p>"
                html += f'<button class="delete-btn" data-id="{product_id}">Delete</button>'

            html += """
            <script>
                document.querySelectorAll(".delete-btn").forEach(button => {
                    button.addEventListener("click", async () => {
                        const id = button.dataset.id;

                        await fetch(`/products/${id}`, {
                            method: "DELETE"
                        });

                        window.location.reload();
                    });
                });
            </script>
            """

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            self.wfile.write(html.encode("utf-8"))

        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()

            self.wfile.write(b"Not found")

    def do_POST(self):
        content_length = self.headers.get("Content-Length")
        result = self.rfile.read(int(content_length))

        decoded_result = result.decode("utf-8")
        clean_data = parse_qs(decoded_result)

        name = clean_data["name"][0]
        price = clean_data["price"][0]

        if self.path == "/products":
            connection = db.get_connection()

            create_product(
                connection,
                name,
                int(price)
            )

            connection.close()

            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        if self.path.startswith("/products/"):
            product_id = int(
                self.path.removeprefix("/products/")
            )

            connection = db.get_connection()

            deleted_rows = delete_product(
                connection,
                product_id
            )

            connection.close()

            if deleted_rows == 1:
                self.send_response(204)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()


server = HTTPServer(("localhost", 8000), MyHandler)

server.serve_forever()