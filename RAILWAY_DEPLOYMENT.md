# Railway Deployment Guide

## Prerequisites
- GitHub account
- Railway account (free at [railway.app](https://railway.app))
- Your code pushed to GitHub

## Step 1: Push Code to GitHub

```bash
cd f:\resume-ai
git init
git add .
git commit -m "Initial commit: Resume AI application"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/resume-ai.git
git push -u origin main
```

## Step 2: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Click "Start New Project"
3. Select "Deploy from GitHub repo"

## Step 3: Connect GitHub

1. Click "Deploy from GitHub repo"
2. Authorize Railway to access your GitHub
3. Select your `resume-ai` repository
4. Click "Deploy Now"

Railway will automatically detect the `Procfile` and `requirements.txt`

## Step 4: Add Environment Variables

1. Go to your Railway project
2. Click on the deployed service (should say "Deploying...")
3. Go to the **Variables** tab
4. Add the following:

```
OPENAI_API_KEY=sk-your-actual-key-here
PROJECT_NAME=Resume AI
API_V1_STR=/api/v1
MAX_UPLOAD_SIZE=10485760
```

## Step 5: Wait for Deployment

- Railway will build and deploy your app
- Check the **Deploy** tab for logs
- Once complete, you'll see a URL like: `https://resume-ai-production.up.railway.app`

## Step 6: Access Your App

Your frontend will be available at the Railway URL provided.

The API will be at: `https://your-railway-url/api/v1`

## Auto-Deployments

Any time you push to GitHub main branch:
```bash
git add .
git commit -m "Your changes"
git push origin main
```

Railway will automatically rebuild and redeploy!

## Troubleshooting

### Check Logs
Railway Dashboard → Deployments → View Logs

### Common Issues

**1. "Module not found" error**
- Make sure `requirements.txt` is at the root
- Run: `pip freeze > requirements.txt` locally and push

**2. "OPENAI_API_KEY not found"**
- Go to Variables tab in Railway
- Add the environment variable
- Restart deployment

**3. Port already in use**
- Railway handles port assignment via `$PORT` environment variable
- Make sure `Procfile` uses `$PORT`: ✓

**4. Frontend not loading**
- Frontend is now served from same domain
- Check that `index.html` exists in `/frontend`
- API calls should automatically use correct domain

## Scale Up (Optional)

In Railway dashboard:
1. Go to your service
2. Click "Settings"
3. Adjust CPU/Memory as needed (paid plans)

## Custom Domain (Optional)

1. Railway Dashboard → Settings
2. Add custom domain
3. Follow DNS instructions
4. Update `CORS` settings in backend if needed

## Next Steps

After deployment, you can:
- Monitor performance in Railway Dashboard
- View logs in real-time
- Set up automatic backups
- Add database if needed (PostgreSQL, MongoDB, etc.)

## Support

- Railway Docs: https://docs.railway.app/
- GitHub Issues: Check your repo
- Contact: support@railway.app
