import os
import psycopg2
from flask import request, jsonify, Response,render_template
from psycopg2.extras import RealDictCursor
from lxml import etree
from TP import app
from TP.db import get_db_connection


# Paths for XML and XSL files (ensure these files are placed alongside this script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'data'))
XML_PATH = os.path.join(DATA_DIR, 'books.xml')
XSL_PATH = os.path.join(DATA_DIR, 'books.xsl')

print(f'BASE_DIR {BASE_DIR}')
print(f'XML_PATH {XML_PATH}')
print(f'XSL_PATH {XSL_PATH}')

def sync_xml_to_db():
    try:
        # Load the XML file
        with open(XML_PATH, 'r', encoding='utf-8') as file:
            xml_content = file.read()

        # Optional: Validate XML structure (this ensures the XML is valid)
        etree.fromstring(xml_content)

        # Connect to the database
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert the XML content into the database
        cur.execute("INSERT INTO books_xml (book_data) VALUES (%s)", (xml_content,))
        conn.commit()  # Commit the transaction to save the data

        print("XML content successfully inserted into the database.")
        return {"message": "XML content successfully inserted into the database."}
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return {"error": str(e)}
    
    finally:
        # Ensure the connection and cursor are properly closed
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route('/')
def index():
    """
    Serve the HTML list of books rendered from the XML file at the root URL.
    """
    try:
        # Parse the XML file to get book data
        xml_doc = etree.parse(XML_PATH)
        livres = xml_doc.xpath('//livre')
        
        books = []
        for livre in livres:
            books.append({
                'id': int(livre.get('id')),
                'titre': livre.findtext('titre'),
                'auteur': livre.findtext('auteur'),
                'annee': livre.findtext('annee'),
                'genre': livre.findtext('genre'),
                'disponible': livre.findtext('disponible'),
            })
        # Render the template and pass the books list to it
        return render_template('index.html', books=books)
    except Exception as e:
        return f"<h1>Error loading books</h1><p>{e}</p>"

@app.route('/books', methods=['GET'])
def search_books():
    title = request.args.get('title', '').lower()
    try:
        xml_doc = etree.parse(XML_PATH)
        livres = xml_doc.xpath(
            f"//livre[contains(translate(titre, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{title}')]"
        )
        books = []
        for livre in livres:
            books.append({
                'id': int(livre.get('id')),
                'titre': livre.findtext('titre'),
                'auteur': livre.findtext('auteur'),
                'annee': livre.findtext('annee'),
                'genre': livre.findtext('genre'),
                'disponible': livre.findtext('disponible'),
            })
        return jsonify(books)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    try:
        # Parse the XML file and search for the book by ID
        xml_doc = etree.parse(XML_PATH)
        livre = xml_doc.xpath(f"//livre[@id='{book_id}']")
        
        if livre:
            livre = livre[0]
            book = {
                'id': int(livre.get('id')),
                'titre': livre.findtext('titre'),
                'auteur': livre.findtext('auteur'),
                'annee': livre.findtext('annee'),
                'genre': livre.findtext('genre'),
                'disponible': livre.findtext('disponible'),
            }
            return jsonify(book)
        return jsonify({'error': 'Book not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        # Parse the XML file and find the book by ID
        xml_doc = etree.parse(XML_PATH)
        livre = xml_doc.xpath(f"//livre[@id='{book_id}']")
        
        if livre:
            # Remove the book element from XML
            root = xml_doc.getroot()
            root.remove(livre[0])
            
            # Save the updated XML
            xml_doc.write(XML_PATH, pretty_print=True, xml_declaration=True, encoding='UTF-8')
            sync_xml_to_db()
            return jsonify({'message': 'Book deleted', 'id': book_id})
        return jsonify({'error': 'Book not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500





@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    required_fields = ['titre', 'auteur', 'annee', 'genre', 'disponible']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    try:
        # Log incoming data for debugging
        print(f"Received data: {data}")
        
        xml_doc = etree.parse(XML_PATH)
        root = xml_doc.getroot()

        # Log XML content before adding
        print(f"Existing XML content: {etree.tostring(root, pretty_print=True).decode()}")

        # Generate a new unique ID
        ids = [int(l.get('id')) for l in root.xpath('//livre') if l.get('id')]
        new_id = max(ids) + 1 if ids else 1

        # Log new ID generation
        print(f"Generated new ID: {new_id}")

        new_livre = etree.SubElement(root, 'livre', id=str(new_id))
        etree.SubElement(new_livre, 'titre').text = data['titre']
        etree.SubElement(new_livre, 'auteur').text = data['auteur']
        etree.SubElement(new_livre, 'annee').text = str(data['annee'])
        etree.SubElement(new_livre, 'genre').text = data['genre']
        etree.SubElement(new_livre, 'disponible').text = data['disponible']

        # Log the new XML content after adding
        print(f"Updated XML content: {etree.tostring(root, pretty_print=True).decode()}")

        xml_doc.write(XML_PATH, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        sync_xml_to_db()

        return jsonify({'message': 'Book added', 'id': new_id}), 201
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 500




@app.route('/books/xml', methods=['GET'])
def xml_books():
    title = request.args.get('title', '').lower()
    try:
        xml_doc = etree.parse(XML_PATH)
        # Fixed f-string to avoid unterminated literal
        expr = f"//livre[contains(translate(titre, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{title}')]"
        livres = xml_doc.xpath(expr)
        books = []
        for livre in livres:
            books.append({
                'id': int(livre.get('id')),
                'titre': livre.findtext('titre'),
                'auteur': livre.findtext('auteur'),
                'annee': livre.findtext('annee'),
                'genre': livre.findtext('genre'),
                'disponible': livre.findtext('disponible'),
            })
        return jsonify(books)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/books/html', methods=['GET'])
def books_html():
    try:
        xml_doc = etree.parse(XML_PATH)
        xsl_doc = etree.parse(XSL_PATH)
        transform = etree.XSLT(xsl_doc)
        result = transform(xml_doc)
        html_bytes = etree.tostring(result, pretty_print=True, encoding='UTF-8')
        return Response(html_bytes, mimetype='text/html; charset=utf-8')
    except Exception as e:
        return Response(f"<h1>Error generating HTML</h1><p>{e}</p>", status=500, mimetype='text/html')

