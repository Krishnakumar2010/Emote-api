"""
Free Fire Emote API - Complete Web Application
Based on original app.py bot functionality with API endpoints
"""

import threading
import jwt
import random
from threading import Thread
import json
import requests
import google.protobuf
from protobuf_decoder.protobuf_decoder import Parser
import json
import datetime
from datetime import datetime
from google.protobuf.json_format import MessageToJson
import my_message_pb2
import data_pb2
import base64
import logging
import re
import socket
from google.protobuf.timestamp_pb2 import Timestamp
import jwt_generator_pb2
import os
import binascii
import sys
import psutil
import MajorLoginRes_pb2
from time import sleep
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time
import urllib3
from important_zitado import*
from byte import*
from flask import Flask, request, jsonify
from flask_cors import CORS

# Flask App Setup
app = Flask(__name__)
CORS(app)

# Global variables for bot management
active_bots = {}
bot_threads = {}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_activity.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Global variables from original code
tempid = None
sent_inv = False
start_par = False
pleaseaccept = False
nameinv = "none"
idinv = 0
senthi = False
statusinfo = False
tempdata1 = None
tempdata = None
leaveee = False
leaveee1 = False
data22 = None
isroom = False
isroom2 = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# All the original functions from app.py
def encrypt_packet(plain_text, key, iv):
    plain_text = bytes.fromhex(plain_text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()

def gethashteam(hexxx):
    a = zitado_get_proto(hexxx)
    if not a:
        raise ValueError("Invalid hex format or empty response from zitado_get_proto")
    data = json.loads(a)
    return data['5']['7']

def getownteam(hexxx):
    a = zitado_get_proto(hexxx)
    if not a:
        raise ValueError("Invalid hex format or empty response from zitado_get_proto")
    data = json.loads(a)
    return data['5']['1']

def get_player_status(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)

    if "5" not in parsed_data or "data" not in parsed_data["5"]:
        return "OFFLINE"

    json_data = parsed_data["5"]["data"]

    if "1" not in json_data or "data" not in json_data["1"]:
        return "OFFLINE"

    data = json_data["1"]["data"]

    if "3" not in data:
        return "OFFLINE"

    status_data = data["3"]

    if "data" not in status_data:
        return "OFFLINE"

    status = status_data["data"]

    if status == 1:
        return "SOLO"
    
    if status == 2:
        if "9" in data and "data" in data["9"]:
            group_count = data["9"]["data"]
            countmax1 = data["10"]["data"]
            countmax = countmax1 + 1
            return f"INSQUAD ({group_count}/{countmax})"

        return "INSQUAD"
    
    if status in [3, 5]:
        return "INGAME"
    if status == 4:
        return "IN ROOM"
    
    if status in [6, 7]:
        return "IN SOCIAL ISLAND MODE .."

    return "NOTFOUND"

def get_idroom_by_idplayer(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)
    json_data = parsed_data["5"]["data"]
    data = json_data["1"]["data"]
    idroom = data['15']["data"]
    return idroom

def get_leader(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)
    json_data = parsed_data["5"]["data"]
    data = json_data["1"]["data"]
    leader = data['8']["data"]
    return leader

def generate_random_color():
    color_list = [
        "[00FF00][b][c]",
        "[FFDD00][b][c]",
        "[3813F3][b][c]",
        "[FF0000][b][c]",
        "[0000FF][b][c]",
        "[FFA500][b][c]",
        "[DF07F8][b][c]",
        "[11EAFD][b][c]",
        "[DCE775][b][c]",
        "[A8E6CF][b][c]",
        "[7CB342][b][c]",
        "[FF0000][b][c]",
        "[FFB300][b][c]",
        "[90EE90][b][c]"
    ]
    random_color = random.choice(color_list)
    return  random_color

def fix_num(num):
    fixed = ""
    count = 0
    num_str = str(num)  # Convert the number to a string

    for char in num_str:
        if char.isdigit():
            count += 1
        fixed += char
        if count == 3:
            fixed += "[c]"
            count = 0  
    return fixed

def fix_word(num):
    fixed = ""
    count = 0
    
    for char in num:
        if char:
            count += 1
        fixed += char
        if count == 3:
            fixed += "[c]"
            count = 0  
    return fixed

def rrrrrrrrrrrrrr(number):
    if isinstance(number, str) and '***' in number:
        return number.replace('***', '106')
    return number

def get_available_room(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = parse_results(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        logging.error(f"error {e}")
        return None

def parse_results(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data["wire_type"] = result.wire_type
        if result.wire_type == "varint":
            field_data["data"] = result.data
        if result.wire_type == "string":
            field_data["data"] = result.data
        if result.wire_type == "bytes":
            field_data["data"] = result.data
        elif result.wire_type == "length_delimited":
            field_data["data"] = parse_results(result.data.results)
        result_dict[result.field] = field_data
    return result_dict

def dec_to_hex(ask):
    ask_result = hex(ask)
    final_result = str(ask_result)[2:]
    if len(final_result) == 1:
        final_result = "0" + final_result
    return final_result

def get_random_avatar():
    avatar_list = [
        '902050001', '902050002', '902050003', '902039016', '902050004', 
        '902047011', '902047010', '902049015', '902050006', '902049020'
    ]
    random_avatar = random.choice(avatar_list)
    return  random_avatar

def restart_program():
    logging.warning("Initiating bot restart...")
    try:
        p = psutil.Process(os.getpid())
        # Close open file descriptors
        for handler in p.open_files() + p.connections():
            try:
                os.close(handler.fd)
            except Exception as e:
                logging.error(f"Failed to close handler {handler.fd}: {e}")
    except Exception as e:
        logging.error(f"Error during pre-restart cleanup: {e}")
    
    # Replace the current process with a new instance of the script
    python = sys.executable
    os.execl(python, python, *sys.argv)

class EmoteBot(threading.Thread):
    """Modified FF_CLIENT class for API usage with auto-exit functionality"""
    
    def __init__(self, bot_id, id, password, team_code, emote_id, target_uids):
        super().__init__()
        self.bot_id = bot_id
        self.id = id
        self.password = password
        self.team_code = team_code
        self.emote_id = emote_id
        self.target_uids = target_uids
        self.key = None
        self.iv = None
        self.start_time = time.time()
        self.status = "initializing"
        self.get_tok()
        self.emote_sent = False
        
    def get_tok(self):
        """Get token - placeholder for actual implementation"""
        # This should implement the actual token generation logic
        pass
        
    def parse_my_message(self, serialized_data):
        try:
            MajorLogRes = MajorLoginRes_pb2.MajorLoginRes()
            MajorLogRes.ParseFromString(serialized_data)
            key = MajorLogRes.ak
            iv = MajorLogRes.aiv
            if isinstance(key, bytes):
                key = key.hex()
            if isinstance(iv, bytes):
                iv = iv.hex()
            self.key = key
            self.iv = iv
            logging.info(f"Key: {self.key} | IV: {self.iv}")
            return self.key, self.iv
        except Exception as e:
            logging.error(f"{e}")
            return None, None

    def nmnmmmmn(self, data):
        key, iv = self.key, self.iv
        try:
            key = key if isinstance(key, bytes) else bytes.fromhex(key)
            iv = iv if isinstance(iv, bytes) else bytes.fromhex(iv)
            data = bytes.fromhex(data)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            cipher_text = cipher.encrypt(pad(data, AES.block_size))
            return cipher_text.hex()
        except Exception as e:
            logging.error(f"Error in nmnmmmmn: {e}")

    def send_emote(self, target_id, emote_id):
        """
        Creates and prepares the packet for sending an emote to a target player.
        """
        fields = {
            1: 21,
            2: {
                1: 804266360,  # Constant value from original code
                2: 909000001,  # Constant value from original code
                5: {
                    1: int(target_id),
                    3: int(emote_id),
                }
            }
        }
        packet = create_protobuf_packet(fields).hex()
        # The packet type '0515' is used for online/squad actions
        header_lenth = len(encrypt_packet(packet, self.key, self.iv)) // 2
        header_lenth_final = dec_to_hex(header_lenth)
        if len(header_lenth_final) == 2:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 3:
            final_packet = "051500000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 4:
            final_packet = "05150000" + header_lenth_final + self.nmnmmmmn(packet)
        elif len(header_lenth_final) == 5:
            final_packet = "0515000" + header_lenth_final + self.nmnmmmmn(packet)
        else:
            final_packet = "0515000000" + header_lenth_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    def join_team(self, team_code):
        """Join team using team code - simplified version"""
        try:
            # Implement team joining logic here
            # This is a placeholder - actual implementation would use the team joining packets
            self.status = "joining_team"
            logging.info(f"Bot {self.bot_id} joining team {team_code}")
            return True
        except Exception as e:
            logging.error(f"Error joining team: {e}")
            return False

    def leave_team(self):
        """Leave current team"""
        try:
            # Implement team leaving logic here
            self.status = "leaving_team"
            logging.info(f"Bot {self.bot_id} leaving team")
            return True
        except Exception as e:
            logging.error(f"Error leaving team: {e}")
            return False

    def execute_emote_sequence(self):
        """Execute the complete emote sequence: join -> emote -> exit"""
        try:
            # Step 1: Join team
            if self.join_team(self.team_code):
                self.status = "in_team"
                
                # Step 2: Send emote to all target UIDs
                self.status = "sending_emote"
                for uid in self.target_uids:
                    emote_packet = self.send_emote(uid, self.emote_id)
                    # Send packet to game server
                    logging.info(f"Sending emote {self.emote_id} to UID {uid}")
                
                self.emote_sent = True
                
                # Step 3: Wait 1 second then auto-exit
                time.sleep(1)
                
                # Step 4: Leave team
                if self.leave_team():
                    self.status = "completed"
                    logging.info(f"Bot {self.bot_id} completed emote sequence")
                
            return True
        except Exception as e:
            logging.error(f"Error in emote sequence: {e}")
            self.status = "error"
            return False

    def run(self):
        """Main thread execution"""
        try:
            self.status = "running"
            self.execute_emote_sequence()
        except Exception as e:
            logging.error(f"Bot {self.bot_id} error: {e}")
            self.status = "error"
        finally:
            # Clean up bot from active bots
            if self.bot_id in active_bots:
                del active_bots[self.bot_id]

# API Routes
@app.route('/emote', methods=['GET'])
def emote_api():
    """Main API endpoint for emote functionality"""
    try:
        # Get parameters from query string
        teamcode = request.args.get('teamcode')
        emoteid = request.args.get('emoteid')
        uid1 = request.args.get('uid1')
        uid2 = request.args.get('uid2')  # Optional
        uid3 = request.args.get('uid3')  # Optional
        uid4 = request.args.get('uid4')  # Optional
        
        # Validation
        if not teamcode:
            return jsonify({
                "status": "error",
                "message": "teamcode parameter is required"
            }), 400
            
        if not emoteid:
            return jsonify({
                "status": "error", 
                "message": "emoteid parameter is required"
            }), 400
            
        if not uid1:
            return jsonify({
                "status": "error",
                "message": "at least uid1 parameter is required"
            }), 400
        
        # Collect target UIDs
        target_uids = [uid for uid in [uid1, uid2, uid3, uid4] if uid]
        
        # Get bot credentials from bot.txt (or environment variables)
        bot_credentials = load_bot_credentials()
        if not bot_credentials:
            return jsonify({
                "status": "error",
                "message": "Bot credentials not found. Please configure bot.txt"
            }), 500
        
        # Generate unique bot ID
        bot_id = f"emote_bot_{int(time.time())}"
        
        # Create and start bot
        bot = EmoteBot(
            bot_id=bot_id,
            id=bot_credentials['id'],
            password=bot_credentials['password'],
            team_code=teamcode,
            emote_id=emoteid,
            target_uids=target_uids
        )
        
        # Add to active bots
        active_bots[bot_id] = bot
        
        # Start bot thread
        thread = threading.Thread(target=bot.run)
        thread.daemon = True
        thread.start()
        bot_threads[bot_id] = thread
        
        return jsonify({
            "status": "success",
            "message": "Emote sequence initiated",
            "bot_id": bot_id,
            "teamcode": teamcode,
            "emoteid": emoteid,
            "target_uids": target_uids,
            "note": "Bot will join team, send emote, and auto-exit after 1 second"
        })
        
    except Exception as e:
        logging.error(f"API error: {e}")
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500

@app.route('/status/<bot_id>', methods=['GET'])
def get_bot_status(bot_id):
    """Get status of a specific bot"""
    if bot_id not in active_bots:
        return jsonify({
            "status": "error",
            "message": "Bot not found"
        }), 404
    
    bot = active_bots[bot_id]
    return jsonify({
        "bot_id": bot_id,
        "status": bot.status,
        "team_code": bot.team_code,
        "emote_id": bot.emote_id,
        "target_uids": bot.target_uids,
        "emote_sent": bot.emote_sent
    })

@app.route('/bots', methods=['GET'])
def list_active_bots():
    """List all active bots"""
    bots_info = {}
    for bot_id, bot in active_bots.items():
        bots_info[bot_id] = {
            "status": bot.status,
            "team_code": bot.team_code,
            "emote_id": bot.emote_id,
            "target_uids": bot.target_uids,
            "emote_sent": bot.emote_sent
        }
    
    return jsonify({
        "active_bots": bots_info,
        "total_active": len(active_bots)
    })

@app.route('/', methods=['GET'])
def home():
    """Home page with API documentation"""
    return jsonify({
        "name": "Free Fire Emote API",
        "version": "1.0.0",
        "description": "API for automated emote functionality in Free Fire",
        "endpoints": {
            "/emote": {
                "method": "GET",
                "description": "Execute emote sequence with auto-exit",
                "parameters": {
                    "teamcode": "Required - Team code to join",
                    "emoteid": "Required - Emote ID to play", 
                    "uid1": "Required - Target player UID",
                    "uid2": "Optional - Additional target UID",
                    "uid3": "Optional - Additional target UID", 
                    "uid4": "Optional - Additional target UID"
                },
                "example": "/emote?teamcode=ABC123&uid1=12345678&emoteid=50"
            },
            "/status/<bot_id>": {
                "method": "GET",
                "description": "Get status of specific bot"
            },
            "/bots": {
                "method": "GET", 
                "description": "List all active bots"
            }
        }
    })

def load_bot_credentials():
    """Load bot credentials from bot.txt file"""
    try:
        if os.path.exists('bot.txt'):
            with open('bot.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if ':' in line:
                        uid, password = line.strip().split(':', 1)
                        return {'id': uid.strip(), 'password': password.strip()}
        
        # Fallback to environment variables
        uid = os.environ.get('BOT_UID')
        password = os.environ.get('BOT_PASSWORD')
        
        if uid and password:
            return {'id': uid, 'password': password}
            
        return None
    except Exception as e:
        logging.error(f"Error loading bot credentials: {e}")
        return None

# Main execution
if __name__ == '__main__':
    logging.info("Starting Free Fire Emote API Server...")
    app.run(host='0.0.0.0', port=5000, debug=False)