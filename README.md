# TCP-Socket-Chat-Room
![](https://img.shields.io/pypi/pyversions/Django?style=plastic)
<a href="https://github.com/DebRC/TCP-Socket-Chat-Room/blob/master/LICENSE">![](https://img.shields.io/apm/l/vim-mode?style=plastic)</a>
<a href="https://realpython.com/python-sockets/">![](https://img.shields.io/badge/Socket%20Programming-%20-yellow)</a>
<a href="https://en.wikipedia.org/wiki/Advanced_Encryption_Standard">![](https://img.shields.io/badge/AES%20Encryption-%20-orange)</a>
<a href="https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange">![](https://img.shields.io/badge/Diffie%20Hellman%20Key%20Exchange-%20-yellow)</a>
<br><br> A GUI-based TCP-Socket-Chat-Room of Client-Server Architecture where messages are encrypted between Client and Server using AES-256 encryption algorithm and symmetric keys are exchanged using Diffie-Hellman method.<br>
A server is set to listening mode, with a specific IP Address and Port numner (can be edited) and clients are made to connect to the server. The messages are then broadcasted to all the clients present. It handles multiple clients using threading.<br>
This project is based on Socket Progamming and Network Security and done using Python.

## ► Working
<ul>
  <li>Server is started and set to listening mode.</li>
  <li>Client is started and TCP-socket connection established between Client-Server.</li> 
  <li>Server asks for Client's Name.</li>
  <li>Client sends it's Name to Server.</li>
  <li>Server and Client both generate public and private keys and exchange the public keys.</li>
  <li>Both generate similar Shared-Private-Key.(Diffie-Hellman-Method)</li>
  <li>Messages send and received between them are encrypted using that key with AES-256 encryption algorithm</li>
  <li>Messages sent from client to server are decrypted using that client's private key</li>
  <li>Then that message is broadcasted to all other clients which is encrypted with their respective keys.</li>
 </ul>
<img align="center" src=https://github.com/DebRC/TCP-Socket-Chat-Room/blob/master/Samples/principle.png height=500px>

## ► Demo
### ◘ Client Interface
![](Samples/client_demo.gif)
### ◘ Working Example with Server
![](Samples/working_demo.gif)
