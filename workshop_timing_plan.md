# Advanced PromQL Labs: 2.5-Hour Workshop Timing Analysis

## 🎯 Workshop Constraints
- **Total Time**: 2.5 hours (150 minutes)
- **Target Audience**: Advanced users
- **Environment**: Killercoda (pre-setup, no installation time)
- **Format**: Quick slide intros + hands-on copy/paste/explore
- **Scope**: Advanced labs only (Labs 5-10)

## 📊 Full Advanced Labs Analysis

| Lab | PromQL Queries | Steps | Challenges | Hands-On Time | Total w/Slides |
|-----|----------------|-------|------------|---------------|----------------|
| Lab5: Advanced CPU Anomaly | 2 | 5 | 1 | 21.0min | 23.5min |
| Lab6: Correlating Metrics | 0 | 6 | 1 | 18.0min | 20.5min |
| Lab7: Recording Rules & Alerting | 1 | 7 | 1 | 22.5min | 25.0min |
| Lab8: Advanced PromQL Operations | 0 | 8 | 1 | 22.0min | 24.5min |
| Lab9: Histograms & Quantiles | 3 | 5 | 1 | 23.5min | 26.0min |
| Lab10: Join Queries & Vector Matching | 2 | 16 | 1 | 43.0min | 45.5min |
| **TOTAL** | **8** | **47** | **6** | **150.0min** | **165.0min** |

## ⚠️ Challenge: Need to Cut 15 Minutes

All labs total **2.8 hours** - need to trim for 2.5-hour constraint.

## 🛠️ Recommended Solutions

### Option 1: Strategic Lab Selection (Recommended)
**Select 5 highest-impact labs**: 140.5 minutes + 9.5 minutes buffer

✅ **Include:**
- **Lab9: Histograms & Quantiles** (26.0min) - 3 queries, essential concept
- **Lab5: Advanced CPU Anomaly** (23.5min) - 2 queries, practical monitoring
- **Lab10: Join Queries & Vector Matching** (45.5min) - 2 queries, advanced skills
- **Lab7: Recording Rules & Alerting** (25.0min) - 1 query, production skills  
- **Lab6: Correlating Metrics** (20.5min) - 0 queries, dashboard building

❌ **Skip:**
- **Lab8: Advanced PromQL Operations** (24.5min) - 0 unique queries, less hands-on

### Option 2: Reduce Slide Time
- Cut slide intros from 2.5min to 1.0min per lab
- **Total**: 156 minutes (2.6 hours) - still 6 minutes over

### Option 3: Speed Up Hands-On Activities  
- Reduce step time from 2.0min to 1.5min each
- Focus on "run and observe" vs "understand deeply"
- **Total**: ~140 minutes

## 🎯 Recommended Workshop Structure (Option 1)

### Block 1: Foundation (48.5 minutes)
1. **Lab5: Advanced CPU Anomaly** (23.5min)
   - 2 PromQL queries + 1 challenge
   - Practical monitoring use case
   - Builds on basic CPU knowledge

2. **Lab6: Correlating Metrics** (20.5min)  
   - Dashboard building focus
   - Visualization techniques
   - No complex queries (breathing room)

3. **5-minute bio break**

### Block 2: Production Skills (45.0 minutes)
4. **Lab7: Recording Rules & Alerting** (25.0min)
   - Production Prometheus setup
   - 1 query + alerting concepts
   - Real-world operational skills

5. **Lab9: Histograms & Quantiles** (26.0min)
   - 3 PromQL queries (most intensive)
   - Advanced statistical concepts
   - Modern observability patterns

### Block 3: Advanced Techniques (47.0 minutes)
6. **Lab10: Join Queries & Vector Matching** (45.5min)
   - 2 complex queries
   - Most advanced PromQL concepts
   - 16 steps (detailed exploration)

**Total**: 140.5 minutes + 5-minute break = 145.5 minutes
**Buffer**: 4.5 minutes for Q&A and overruns

## ⏱️ Timing Assumptions

### Per Activity Type:
- **Simple PromQL Query**: 1.0 minute (copy/paste/run/observe)
- **Complex PromQL Query**: 2.5 minutes (copy/paste/run/understand)
- **Numbered Instruction**: 2.0 minutes (read/execute/observe)  
- **Challenge Section**: 4.0 minutes (explore/experiment)
- **Solution Review**: 2.0 minutes (if showing solutions)
- **Slide Intro**: 2.5 minutes (quick concept overview)

### Workshop Flow:
- **Copy/paste focused**: Minimal typing, maximum exploration
- **Quick explanations**: Context without deep theory
- **Immediate feedback**: Students see results quickly

## 🚨 Risk Mitigation

### If Running Behind:
1. **Skip challenge sections** (-6 minutes total)
2. **Show solutions without student exploration** (-12 minutes total)
3. **Reduce slide intros to 1 minute** (-9 minutes total)
4. **Skip Lab6** if needed (-20.5 minutes total)

### If Running Ahead:
1. **Deep-dive into Lab10 advanced scenarios**
2. **Show Lab8 as bonus content**
3. **Extended Q&A on production PromQL**
4. **Live troubleshooting of complex queries**

## 💡 Success Factors

### For Instructors:
- **Pre-test all queries** in Killercoda environment
- **Have backup simple queries** ready if complex ones fail
- **Master copy/paste workflow** to help stuck students quickly
- **Know which steps can be skipped** if time pressures arise

### For Students:
- **Killercoda accounts ready** (environment running before session)
- **Familiarity with basic PromQL** (prerequisite check)
- **Copy/paste skills** (minimize typing errors)
- **Grafana basic navigation** (dashboard creation skills)

---

**Recommended Decision**: Use Option 1 (Strategic Lab Selection) for the most balanced workshop experience with proper buffer time and comprehensive coverage of advanced PromQL concepts.
