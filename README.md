# TCP-Socket-Chat-Room
![](https://img.shields.io/apm/l/vim-mode?style=plastic)
![](https://img.shields.io/pypi/pyversions/Django?style=plastic)
<br><br> A GUI-based TCP-Socket-Chat-Room of Client-Server Architecture where messages are encrypted between Client and Server using AES-256 encryption algorithm and symmetric keys are exchanged using Diffie-Hellman method.<br>
A server is set to listening mode, with a specific IP Address and Port numner (can be edited) and clients are made to connect to the server. The messages are then broadcasted to all the clients present.<br>
This project is based on Socket Progamming and Network Security and done using Python.

## ► Working
<ul>
  <li>Server is started and set to listening mode.</li>
  <li>Client is started and TCP-socket connection established between Client-Server.</li> 
  <li>Server asks for Client's Name.</li>
  <li>Client sends Name to Server.</li>
  <li>Server and Client both generate public keys and exchange them.</li>
  <li>Both generate Shared-Private-Key.(Diffie-Hellman-Method)</li>
  <li>Messages send and received between them are encrypted using that key with AES-256 encryption algorithm</li>
 </ul>
<img align="center" src=https://github.com/DebRC/TCP-Socket-Chat-Room/blob/master/Samples/principle.png height=500px>
<!-- ## ► Client Interface. It handles multiple clients using threading.
![](client_demo.gif)
### ◘ Working Example with Server
![](working_demo.gif) -->
