# Railway Deployment Checklist ✓

## Pre-Deployment (COMPLETED)

- [x] Create Procfile
- [x] Create runtime.txt  
- [x] Update app/main.py to serve frontend
- [x] Update frontend/script.js for auto-detection
- [x] Create deployment documentation
- [x] Commit all changes to GitHub
- [x] Push to GitHub main branch

## Deployment Steps

### Step 1: Visit Railway (2 min)
- [ ] Go to https://railway.app
- [ ] Sign up with GitHub
- [ ] Authorize Railway

### Step 2: Deploy (3 min)
- [ ] Click "Create New Project"
- [ ] Select "Deploy from GitHub repo"
- [ ] Select "resume-ai" repository
- [ ] Click "Deploy Now"
- [ ] Wait for build to complete

### Step 3: Configure (2 min)
- [ ] Click on the deployed service
- [ ] Go to "Variables" tab
- [ ] Add: OPENAI_API_KEY = sk-your-key
- [ ] Add: PROJECT_NAME = Resume AI
- [ ] Add: API_V1_STR = /api/v1
- [ ] Add: MAX_UPLOAD_SIZE = 10485760
- [ ] Restart deployment

### Step 4: Verify (1 min)
- [ ] Get public URL from Railway
- [ ] Click the URL in browser
- [ ] See Resume AI frontend load
- [ ] Try uploading a resume
- [ ] Test "Analyze Resume" button

## Post-Deployment

### Optional: Custom Domain
- [ ] Go to Railway Settings
- [ ] Add custom domain
- [ ] Configure DNS records
- [ ] Update CORS if needed

### Optional: Monitoring
- [ ] Enable error tracking (Sentry)
- [ ] Set up alerts
- [ ] Monitor logs daily

### Maintenance
- [ ] Update code → Push to GitHub
- [ ] Railway auto-deploys
- [ ] Check logs after each deploy
- [ ] Monitor performance

## Expected Timeline

| Step | Time | Status |
|------|------|--------|
| Sign up to Railway | 2 min | ⏱️ |
| Deploy from GitHub | 3 min | ⏱️ |
| Add environment variables | 2 min | ⏱️ |
| Build & deploy | 2-3 min | ⏱️ |
| **Total** | **~10 minutes** | ⏱️ |

## Success Indicators

Once deployed, you should see:
- ✓ Frontend loads without errors
- ✓ "Analyze Resume" button works
- ✓ File upload works
- ✓ "Refine Resume" button works
- ✓ No 404 errors in console
- ✓ API calls go to same domain (not localhost)

## Troubleshooting

### Issue: Build fails
**Solution:** Check Railway logs for error, ensure requirements.txt is valid

### Issue: Frontend won't load
**Solution:** Verify index.html exists in frontend/

### Issue: API fails "Failed to fetch"
**Solution:** Check OPENAI_API_KEY is set in Railway Variables

### Issue: Refine button doesn't work
**Solution:** Verify OPENAI_API_KEY is valid and set

## After First Deployment

1. **Test everything locally first:**
   ```bash
   uvicorn app.main:app --port 8000
   ```

2. **Make a test resume upload**
   - Test with dummy resume
   - Test with real job description
   - Verify all features work

3. **Monitor Railway dashboard**
   - Watch logs for errors
   - Check CPU/memory usage
   - Note any issues

4. **Share with others**
   - Copy public URL
   - Send to friends/colleagues
   - Gather feedback

## Keep in Mind

- Railway free tier has limits (~500 hrs/month)
- Static files (frontend) served very fast (CDN)
- API scales automatically with demand
- Logs available for 24 hours
- Free tier suitable for development/testing
- Paid tier ($5+/month) for production

## GitHub Integration

Railway watches your GitHub repo:
- Any push to `main` branch → Auto-deploy
- No manual rebuilds needed
- Perfect for continuous deployment
- Easy rollback if needed

## URLs to Bookmark

- Railway Dashboard: https://railway.app
- GitHub Repo: https://github.com/cobrianz/resume-ai
- Your App: (provided by Railway)
- API Docs: https://your-app-url/docs

## Questions?

- **Railway Help:** https://docs.railway.app/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **My Notes:** See RAILWAY_QUICK_START.md

---

**Status:** ✅ READY FOR DEPLOYMENT

Your Resume AI is fully configured and ready to deploy to Railway!
Follow the steps above to get it live in ~10 minutes.
