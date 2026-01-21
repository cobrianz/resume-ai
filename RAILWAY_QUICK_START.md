# Railway Deployment - Step by Step

## Your Resume AI is Ready for Railway! ✓

All configuration files are in place:
- ✓ `Procfile` - Deployment instructions
- ✓ `runtime.txt` - Python version
- ✓ `requirements.txt` - Dependencies
- ✓ Updated `app/main.py` - Serves frontend + API
- ✓ Updated `frontend/script.js` - Auto-detects API endpoint

---

## Deploy in 5 Minutes

### Step 1: Ensure Code is on GitHub

Check your GitHub repo has the latest code:
```bash
git push origin main
```

### Step 2: Go to Railway.app

1. Visit **https://railway.app**
2. Sign up with GitHub (easy login)
3. Click **"Create a new Project"**

### Step 3: Deploy from GitHub

1. Click **"Deploy from GitHub repo"**
2. Authorize Railway to access your GitHub
3. Select your **resume-ai** repository
4. Click **"Deploy Now"**

Railway will start building automatically!

### Step 4: Add Environment Variables

While Railway is deploying:

1. Click on your deployed service
2. Go to **"Variables"** tab
3. Add these variables:

```
OPENAI_API_KEY = sk-proj-your-actual-openai-key
PROJECT_NAME = Resume AI
API_V1_STR = /api/v1
MAX_UPLOAD_SIZE = 10485760
```

**Important:** Replace `sk-proj-...` with your actual OpenAI API key

### Step 5: Wait for Build to Complete

- Go to **"Deployments"** tab
- Watch for green checkmark ✓
- Takes usually 2-3 minutes

### Step 6: Access Your App

Once deployed:
1. Click on your service
2. Look for "**Public URL**" 
3. Your app is live at that URL!

Example: `https://resume-ai-production.up.railway.app`

---

## What's Included

✓ **Frontend** - Served directly from Railway  
✓ **Backend API** - FastAPI on same domain  
✓ **Auto-CORS** - Frontend and API talk seamlessly  
✓ **Auto-Updates** - Push to GitHub → Auto-deploy  

---

## Features

### Auto-Deployments (Magic!)

Every time you push to GitHub:
```bash
git add .
git commit -m "Your changes"
git push origin main
```

Railway automatically redeploys! No manual steps needed.

### View Logs
- Railway Dashboard → Deployments → View Logs
- See errors in real-time

### Monitor Performance
- CPU/Memory usage
- Request count
- Deploy history

### Scale (Paid)
- Click Settings → Adjust CPU/Memory
- Paid plans start at $5/month

---

## Troubleshooting

### App Won't Start
```
Check Logs in Railway Dashboard
Look for: "ModuleNotFoundError" or "ImportError"
```

### CORS/API Errors
```
Make sure OPENAI_API_KEY is set in Variables
Restart the deployment
```

### Frontend Not Loading
```
API should auto-detect endpoint
If issues, check browser console (F12 → Network tab)
```

### Need Help?
1. Check Railway Logs (easiest)
2. Check `.env` file locally
3. Run locally first: `uvicorn app.main:app`

---

## After Deployment

### Custom Domain (Optional)
1. Railway Settings → Domains
2. Add your custom domain
3. Follow DNS instructions

### Database (Optional)
1. New Project → Add PostgreSQL/MongoDB
2. Railway auto-configures connections
3. All variables available to app

### Monitoring (Optional)
1. Enable Sentry integration for error tracking
2. Add Analytics
3. Set up alerts

---

## Summary

Your app is now:
- ✓ Deployed globally on Railway CDN
- ✓ Auto-updating on every GitHub push
- ✓ Serving frontend + API from same domain
- ✓ Automatically scaled and load-balanced
- ✓ Production-ready with error tracking

**Estimated cost:** $0-5/month depending on usage

Enjoy! 🚀
