#!/usr/bin/env python3
"""
Local SEO Manager
Comprehensive local SEO management and optimization tool.
"""

from flask import Flask, render_template_string, jsonify, request
import json
from datetime import datetime
import re

app = Flask(__name__)

class LocalSEOManager:
    def __init__(self):
        self.business_data = {
            'name': 'Example Local Business',
            'address': '123 Main Street, City, State 12345',
            'phone': '+1-555-123-4567',
            'website': 'https://example.com',
            'category': 'Restaurant',
            'hours': {
                'monday': '9:00 AM - 9:00 PM',
                'tuesday': '9:00 AM - 9:00 PM',
                'wednesday': '9:00 AM - 9:00 PM',
                'thursday': '9:00 AM - 9:00 PM',
                'friday': '9:00 AM - 10:00 PM',
                'saturday': '9:00 AM - 10:00 PM',
                'sunday': '10:00 AM - 8:00 PM'
            }
        }
        
        self.citations = [
            {'platform': 'Google My Business', 'status': 'verified', 'url': 'https://business.google.com'},
            {'platform': 'Yelp', 'status': 'claimed', 'url': 'https://yelp.com'},
            {'platform': 'Facebook', 'status': 'active', 'url': 'https://facebook.com'},
            {'platform': 'Yellow Pages', 'status': 'pending', 'url': 'https://yellowpages.com'},
            {'platform': 'Bing Places', 'status': 'verified', 'url': 'https://bing.com/places'}
        ]
        
        self.keywords = [
            {'keyword': 'best restaurant near me', 'volume': 1200, 'difficulty': 65, 'rank': 8},
            {'keyword': 'italian food downtown', 'volume': 800, 'difficulty': 45, 'rank': 3},
            {'keyword': 'family restaurant', 'volume': 950, 'difficulty': 55, 'rank': 12},
            {'keyword': 'pizza delivery', 'volume': 1500, 'difficulty': 70, 'rank': 15},
            {'keyword': 'romantic dinner spot', 'volume': 600, 'difficulty': 40, 'rank': 5}
        ]
    
    def get_seo_score(self):
        # Calculate overall SEO score based on various factors
        verified_citations = len([c for c in self.citations if c['status'] == 'verified'])
        total_citations = len(self.citations)
        citation_score = (verified_citations / total_citations) * 30
        
        # Keyword ranking score
        avg_rank = sum([k['rank'] for k in self.keywords]) / len(self.keywords)
        ranking_score = max(0, (20 - avg_rank) / 20 * 40)
        
        # Business info completeness
        info_score = 30  # Assuming complete info
        
        return min(100, citation_score + ranking_score + info_score)
    
    def get_recommendations(self):
        recommendations = []
        
        # Citation recommendations
        pending_citations = [c for c in self.citations if c['status'] == 'pending']
        if pending_citations:
            recommendations.append({
                'type': 'Citations',
                'priority': 'High',
                'action': f'Complete verification for {len(pending_citations)} pending citations',
                'impact': 'Improve local search visibility'
            })
        
        # Keyword recommendations
        poor_rankings = [k for k in self.keywords if k['rank'] > 10]
        if poor_rankings:
            recommendations.append({
                'type': 'Keywords',
                'priority': 'Medium',
                'action': f'Optimize content for {len(poor_rankings)} underperforming keywords',
                'impact': 'Increase organic traffic'
            })
        
        # Review recommendations
        recommendations.append({
            'type': 'Reviews',
            'priority': 'High',
            'action': 'Implement review generation strategy',
            'impact': 'Boost local rankings and trust'
        })
        
        return recommendations

manager = LocalSEOManager()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local SEO Manager</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header { background: white; border-radius: 15px; padding: 30px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; }
        .dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .card { background: white; border-radius: 15px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; padding: 25px; text-align: center; }
        .metric-value { font-size: 2.5rem; font-weight: bold; margin-bottom: 10px; }
        .metric-label { font-size: 1rem; opacity: 0.9; }
        .btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: 600; margin: 5px; }
        .btn:hover { opacity: 0.9; }
        .data-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        .data-table th, .data-table td { padding: 12px; text-align: left; border-bottom: 1px solid #e0e0e0; }
        .data-table th { background: #f8f9fa; font-weight: 600; }
        .status-verified { color: #27ae60; font-weight: bold; }
        .status-claimed { color: #3498db; font-weight: bold; }
        .status-active { color: #27ae60; font-weight: bold; }
        .status-pending { color: #f39c12; font-weight: bold; }
        .priority-high { color: #e74c3c; font-weight: bold; }
        .priority-medium { color: #f39c12; font-weight: bold; }
        .priority-low { color: #27ae60; font-weight: bold; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 10px; border: 2px solid #e0e0e0; border-radius: 8px; }
        .progress-bar { background: #e0e0e0; border-radius: 10px; height: 20px; overflow: hidden; margin-top: 10px; }
        .progress-fill { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 100%; transition: width 0.3s ease; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📍 Local SEO Manager</h1>
            <p>Comprehensive local SEO management and optimization tool</p>
        </div>
        
        <div class="dashboard-grid">
            <div class="metric-card">
                <div class="metric-value" id="seoScore">--</div>
                <div class="metric-label">SEO Score</div>
                <div class="progress-bar">
                    <div class="progress-fill" id="seoProgress" style="width: 0%"></div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-value" id="citationCount">--</div>
                <div class="metric-label">Active Citations</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-value" id="keywordCount">--</div>
                <div class="metric-label">Tracked Keywords</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-value" id="avgRank">--</div>
                <div class="metric-label">Avg. Keyword Rank</div>
            </div>
        </div>
        
        <div class="dashboard-grid">
            <div class="card">
                <h3>🏢 Business Information</h3>
                <button onclick="editBusiness()" class="btn">✏️ Edit Business Info</button>
                <div id="businessInfo">
                    <!-- Business info will be populated here -->
                </div>
            </div>
            
            <div class="card">
                <h3>💡 SEO Recommendations</h3>
                <button onclick="loadRecommendations()" class="btn">🔄 Refresh</button>
                <div id="recommendations">
                    <!-- Recommendations will be populated here -->
                </div>
            </div>
        </div>
        
        <div class="card">
            <h3>📋 Citation Management</h3>
            <button onclick="loadCitations()" class="btn">🔄 Refresh Citations</button>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Platform</th>
                        <th>Status</th>
                        <th>URL</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="citationsBody">
                    <!-- Citations will be populated here -->
                </tbody>
            </table>
        </div>
        
        <div class="card">
            <h3>🔍 Keyword Tracking</h3>
            <button onclick="loadKeywords()" class="btn">🔄 Refresh Keywords</button>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Keyword</th>
                        <th>Search Volume</th>
                        <th>Difficulty</th>
                        <th>Current Rank</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="keywordsBody">
                    <!-- Keywords will be populated here -->
                </tbody>
            </table>
        </div>
    </div>

    <script>
        async function loadDashboard() {
            try {
                const response = await fetch('/api/dashboard');
                const data = await response.json();
                
                document.getElementById('seoScore').textContent = Math.round(data.seo_score);
                document.getElementById('seoProgress').style.width = data.seo_score + '%';
                document.getElementById('citationCount').textContent = data.citation_count;
                document.getElementById('keywordCount').textContent = data.keyword_count;
                document.getElementById('avgRank').textContent = data.avg_rank.toFixed(1);
                
                // Load business info
                const businessInfo = document.getElementById('businessInfo');
                businessInfo.innerHTML = `
                    <p><strong>Name:</strong> ${data.business.name}</p>
                    <p><strong>Address:</strong> ${data.business.address}</p>
                    <p><strong>Phone:</strong> ${data.business.phone}</p>
                    <p><strong>Website:</strong> <a href="${data.business.website}" target="_blank">${data.business.website}</a></p>
                    <p><strong>Category:</strong> ${data.business.category}</p>
                `;
                
            } catch (error) {
                console.error('Error loading dashboard:', error);
            }
        }
        
        async function loadCitations() {
            try {
                const response = await fetch('/api/citations');
                const citations = await response.json();
                
                document.getElementById('citationsBody').innerHTML = citations.map(citation => `
                    <tr>
                        <td><strong>${citation.platform}</strong></td>
                        <td class="status-${citation.status}">${citation.status.toUpperCase()}</td>
                        <td><a href="${citation.url}" target="_blank">View Profile</a></td>
                        <td><button class="btn" onclick="manageCitation('${citation.platform}')">Manage</button></td>
                    </tr>
                `).join('');
            } catch (error) {
                console.error('Error loading citations:', error);
            }
        }
        
        async function loadKeywords() {
            try {
                const response = await fetch('/api/keywords');
                const keywords = await response.json();
                
                document.getElementById('keywordsBody').innerHTML = keywords.map(keyword => `
                    <tr>
                        <td><strong>${keyword.keyword}</strong></td>
                        <td>${keyword.volume.toLocaleString()}</td>
                        <td>${keyword.difficulty}%</td>
                        <td>#${keyword.rank}</td>
                        <td><button class="btn" onclick="optimizeKeyword('${keyword.keyword}')">Optimize</button></td>
                    </tr>
                `).join('');
            } catch (error) {
                console.error('Error loading keywords:', error);
            }
        }
        
        async function loadRecommendations() {
            try {
                const response = await fetch('/api/recommendations');
                const recommendations = await response.json();
                
                document.getElementById('recommendations').innerHTML = recommendations.map(rec => `
                    <div style="padding: 15px; border-left: 4px solid #667eea; margin-bottom: 15px; background: #f8f9fa; border-radius: 0 8px 8px 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <strong>${rec.type}</strong>
                            <span class="priority-${rec.priority.toLowerCase()}">${rec.priority} Priority</span>
                        </div>
                        <div style="margin-bottom: 10px;">${rec.action}</div>
                        <div style="font-size: 14px; color: #666;"><strong>Impact:</strong> ${rec.impact}</div>
                    </div>
                `).join('');
            } catch (error) {
                console.error('Error loading recommendations:', error);
            }
        }
        
        function editBusiness() {
            alert('Business editing feature - Coming soon!');
        }
        
        function manageCitation(platform) {
            alert(`Managing ${platform} citation - Feature coming soon!`);
        }
        
        function optimizeKeyword(keyword) {
            alert(`Optimizing for "${keyword}" - Feature coming soon!`);
        }
        
        // Load data on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadDashboard();
            loadCitations();
            loadKeywords();
            loadRecommendations();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/dashboard')
def get_dashboard():
    seo_score = manager.get_seo_score()
    citation_count = len([c for c in manager.citations if c['status'] in ['verified', 'claimed', 'active']])
    keyword_count = len(manager.keywords)
    avg_rank = sum([k['rank'] for k in manager.keywords]) / len(manager.keywords)
    
    return jsonify({
        'seo_score': seo_score,
        'citation_count': citation_count,
        'keyword_count': keyword_count,
        'avg_rank': avg_rank,
        'business': manager.business_data
    })

@app.route('/api/citations')
def get_citations():
    return jsonify(manager.citations)

@app.route('/api/keywords')
def get_keywords():
    return jsonify(manager.keywords)

@app.route('/api/recommendations')
def get_recommendations():
    return jsonify(manager.get_recommendations())

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

