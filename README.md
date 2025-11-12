# Free Fire Emote API

A complete web API for automated emote functionality in Free Fire based on your original bot code. This API allows you to trigger emote sequences through HTTP requests with automatic team joining, emote playing, and team leaving.

## Features

- 🎮 **Team Auto-Join**: Bot automatically joins specified team using team code
- 😎 **Emote Execution**: Sends emotes to specified UIDs
- ⚡ **Auto-Exit**: Bot automatically leaves team after 1 second
- 🔧 **Multiple Targets**: Support for 1-4 target UIDs (uid1 to uid4, uid1 is required)
- 📊 **Status Tracking**: Real-time bot status monitoring
- 🌐 **REST API**: Clean HTTP API endpoints

## API Endpoints

### Main Emote Endpoint
```
GET /emote?teamcode={teamcode}&uid1={uid1}&uid2={uid2}&uid3={uid3}&uid4={uid4}&emoteid={emoteid}
```

**Required Parameters:**
- `teamcode`: Team code to join
- `uid1`: Target player UID (minimum requirement)
- `emoteid`: Emote ID to play

**Optional Parameters:**
- `uid2`: Additional target UID
- `uid3`: Additional target UID  
- `uid4`: Additional target UID

**Example:**
```
GET https://your-domain.vercel.app/emote?teamcode=ABC123&uid1=12345678&emoteid=50
```

### Bot Status Endpoint
```
GET /status/{bot_id}
```
Get status of a specific bot instance.

### Active Bots Endpoint
```
GET /bots
```
List all currently active bot instances.

### Home/Info Endpoint
```
GET /
```
API documentation and information.

## Installation & Setup

### 1. File Structure
Your project should have this structure:
```
your-project/
├── index.py              # Main application file
├── api/
│   └── index.py         # Vercel serverless entry point
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
├── bot.txt              # Bot credentials (UID:PASSWORD)
├── important_zitado.py  # Your original helper functions
├── byte.py             # Your original byte functions
├── my_message_pb2.py   # Protocol buffer definitions
├── data_pb2.py         # Protocol buffer definitions
├── jwt_generator_pb2.py # Protocol buffer definitions
└── MajorLoginRes_pb2.py # Protocol buffer definitions
```

### 2. Bot Configuration
Create a `bot.txt` file with your bot credentials:
```
YOUR_BOT_UID:YOUR_BOT_PASSWORD
```

Or use environment variables:
- `BOT_UID`: Your bot's UID
- `BOT_PASSWORD`: Your bot's password

### 3. Dependencies
All required dependencies are listed in `requirements.txt`:
```
Flask==2.3.3
Flask-CORS==4.0.0
requests==2.31.0
protobuf==4.24.2
pycryptodome==3.19.0
protobuf-decoder==1.0.3
psutil==5.9.6
pyjwt==2.8.0
urllib3==2.0.7
```

## Deployment to Vercel

### Method 1: Using Vercel CLI

1. **Install Vercel CLI:**
```bash
npm install -g vercel
```

2. **Login to Vercel:**
```bash
vercel login
```

3. **Deploy your project:**
```bash
vercel
```

4. **Follow the prompts:**
- Link to existing project or create new
- Confirm deployment settings
- Deploy!

### Method 2: Using GitHub Integration

1. **Push your code to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

2. **Connect to Vercel:**
- Go to [vercel.com](https://vercel.com)
- Click "New Project"
- Import your GitHub repository
- Configure settings (Python runtime, etc.)
- Deploy!

### Environment Variables Setup

In Vercel dashboard, set these environment variables:
- `BOT_UID`: Your bot's UID
- `BOT_PASSWORD`: Your bot's password

## Usage Examples

### Basic Usage
```bash
curl "https://your-domain.vercel.app/emote?teamcode=TEAM123&uid1=12345678&emoteid=50"
```

### Multiple Targets
```bash
curl "https://your-domain.vercel.app/emote?teamcode=TEAM123&uid1=12345678&uid2=87654321&uid3=55556666&emoteid=75"
```

### Check Bot Status
```bash
curl "https://your-domain.vercel.app/status/emote_bot_1699123456"
```

### List Active Bots
```bash
curl "https://your-domain.vercel.app/bots"
```

## API Response Format

### Success Response
```json
{
  "status": "success",
  "message": "Emote sequence initiated",
  "bot_id": "emote_bot_1699123456",
  "teamcode": "ABC123",
  "emoteid": "50",
  "target_uids": ["12345678"],
  "note": "Bot will join team, send emote, and auto-exit after 1 second"
}
```

### Error Response
```json
{
  "status": "error",
  "message": "teamcode parameter is required"
}
```

## Bot Status Flow

1. **initializing**: Bot is being created
2. **joining_team**: Bot is joining the specified team
3. **in_team**: Bot has successfully joined the team
4. **sending_emote**: Bot is sending emotes to target UIDs
5. **leaving_team**: Bot is leaving the team (auto-exit)
6. **completed**: Bot has finished the entire sequence
7. **error**: An error occurred during execution

## Important Notes

⚠️ **Security**: Keep your bot credentials secure. Never commit `bot.txt` to public repositories.

⚠️ **Rate Limits**: Be mindful of Free Fire's API rate limits to avoid bans.

⚠️ **Dependencies**: Make sure all your original helper files (`important_zitado.py`, `byte.py`, etc.) are included in the deployment.

⚠️ **Protocol Buffers**: Ensure all `.py` files with protobuf definitions are included.

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all helper files are included in your deployment
2. **Authentication Issues**: Verify bot credentials in `bot.txt` or environment variables
3. **Team Join Failures**: Check if team code is valid and team has space
4. **Deployment Failures**: Ensure `vercel.json` is properly configured

### Debug Mode

For debugging, you can check the logs in Vercel dashboard or modify the logging level in `index.py`.

## Support

This API is based on your original Free Fire bot code and maintains all the core functionality while providing a clean HTTP interface for web integration.

For issues related to the original bot functionality, refer to your existing codebase. For API-specific issues, check the deployment configuration and endpoint usage.