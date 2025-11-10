from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # 允许跨域请求

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS contacts
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT NOT NULL,
         phone TEXT NOT NULL,
         email TEXT)
    ''')
    conn.commit()
    conn.close()

@app.route('/contacts', methods=['GET'])
def get_contacts():
    """获取所有联系人"""
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('SELECT * FROM contacts')
    contacts = [{'id': row[0], 'name': row[1], 'phone': row[2], 'email': row[3]} for row in c.fetchall()]
    conn.close()
    return jsonify(contacts)

@app.route('/contacts', methods=['POST'])
def add_contact():
    """添加联系人"""
    data = request.json
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)',
              (data['name'], data['phone'], data.get('email', '')))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Contact added successfully'})

@app.route('/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    """更新联系人"""
    data = request.json
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('UPDATE contacts SET name=?, phone=?, email=? WHERE id=?',
              (data['name'], data['phone'], data.get('email', ''), contact_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Contact updated successfully'})

@app.route('/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """删除联系人"""
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('DELETE FROM contacts WHERE id=?', (contact_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Contact deleted successfully'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
