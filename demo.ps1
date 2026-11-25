# OpenFunds v2.0 - Interactive Demo Script
# This script demonstrates all API features

param(
    [switch]$Clean,
    [switch]$ShowStats,
    [switch]$CreateDemoData
)

$baseUrl = "http://localhost:5000/api/v1"

function Write-Section {
    param([string]$Title)
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host " $Title" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Cyan
}

function Test-Backend {
    Write-Section "Testing Backend Connection"
    try {
        $health = Invoke-RestMethod -Uri "$baseUrl/health" -TimeoutSec 3
        Write-Host "✅ Backend Status: $($health.status)" -ForegroundColor Green
        Write-Host "   Service: $($health.service)" -ForegroundColor White
        Write-Host "   Version: $($health.version)" -ForegroundColor White
        return $true
    } catch {
        Write-Host "❌ Backend is not running!" -ForegroundColor Red
        Write-Host "   Start it with: cd backend; python run.py" -ForegroundColor Yellow
        return $false
    }
}

function Show-Statistics {
    Write-Section "Platform Statistics"
    try {
        $stats = Invoke-RestMethod -Uri "$baseUrl/campaigns/stats"
        $s = $stats.statistics
        
        Write-Host "📊 Campaigns:" -ForegroundColor Yellow
        Write-Host "   Total:    $($s.total_campaigns)" -ForegroundColor White
        Write-Host "   Active:   $($s.active_campaigns)" -ForegroundColor Green
        Write-Host "   Funded:   $($s.funded_campaigns)" -ForegroundColor Blue
        
        Write-Host "`n💰 Fundraising:" -ForegroundColor Yellow
        Write-Host "   Raised:   $($s.total_raised) BTC" -ForegroundColor Green
        Write-Host "   Target:   $($s.total_target) BTC" -ForegroundColor White
        Write-Host "   Progress: $($s.platform_progress)%" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Could not fetch statistics" -ForegroundColor Red
    }
}

function Show-Campaigns {
    Write-Section "All Campaigns"
    try {
        $result = Invoke-RestMethod -Uri "$baseUrl/campaigns"
        $campaigns = $result.campaigns
        
        if ($campaigns.Count -eq 0) {
            Write-Host "   No campaigns yet. Create one!" -ForegroundColor Yellow
        } else {
            foreach ($c in $campaigns) {
                $progress = [math]::Round(($c.current_amount / $c.target_amount) * 100, 1)
                Write-Host "`n📋 Campaign #$($c.id): " -NoNewline -ForegroundColor Cyan
                Write-Host "$($c.title)" -ForegroundColor White
                Write-Host "   Owner:    $($c.owner_name)" -ForegroundColor Gray
                Write-Host "   Status:   $($c.status)" -ForegroundColor $(if($c.status -eq "Active"){"Green"}elseif($c.status -eq "Funded"){"Blue"}else{"Gray"})
                Write-Host "   Progress: $($c.current_amount)/$($c.target_amount) BTC ($progress%)" -ForegroundColor Yellow
                Write-Host "   Address:  $($c.btc_address)" -ForegroundColor DarkGray
            }
        }
    } catch {
        Write-Host "❌ Could not fetch campaigns" -ForegroundColor Red
    }
}

function Create-DemoData {
    Write-Section "Creating Demo Data"
    
    # Register user
    Write-Host "1. Creating demo user..." -ForegroundColor Yellow
    try {
        $register = Invoke-RestMethod -Uri "$baseUrl/auth/register" -Method POST -ContentType "application/json" -Body (@{
            name = "Demo User"
            email = "demo@test.com"
            password = "demo123"
        } | ConvertTo-Json)
        Write-Host "   ✅ User created: $($register.user.name)" -ForegroundColor Green
    } catch {
        Write-Host "   ⚠️  User might already exist" -ForegroundColor Yellow
    }
    
    # Login
    Write-Host "`n2. Logging in..." -ForegroundColor Yellow
    $login = Invoke-RestMethod -Uri "$baseUrl/auth/login" -Method POST -ContentType "application/json" -Body (@{
        email = "demo@test.com"
        password = "demo123"
    } | ConvertTo-Json)
    
    $token = $login.access_token
    Write-Host "   ✅ Token obtained" -ForegroundColor Green
    
    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }
    
    # Create campaigns
    Write-Host "`n3. Creating sample campaigns..." -ForegroundColor Yellow
    
    $sampleCampaigns = @(
        @{
            title = "Community Garden Project"
            description = "Building a sustainable community garden to grow fresh produce for local families"
            btc_address = "2N8hwP1WmJrFF5QWABn38y63uYLhnJYJYTF"
            target_amount = 1.0
        },
        @{
            title = "Tech Education for Kids"
            description = "Providing free coding classes and laptops to underprivileged children"
            btc_address = "2MzQwSSnBHWHqSAqtTVQ6v47XtaisrJa1Vc"
            target_amount = 2.0
        },
        @{
            title = "Animal Rescue Center"
            description = "Supporting our local animal shelter with medical supplies and food"
            btc_address = "2N4QFkKac8JQ6YQTN9V3kWYwnEfJ7FWjRqy"
            target_amount = 1.5
        }
    )
    
    foreach ($campaign in $sampleCampaigns) {
        try {
            $result = Invoke-RestMethod -Uri "$baseUrl/campaigns" -Method POST -Headers $headers -Body ($campaign | ConvertTo-Json)
            Write-Host "   ✅ Created: $($result.campaign.title)" -ForegroundColor Green
        } catch {
            Write-Host "   ⚠️  Could not create: $($campaign.title)" -ForegroundColor Yellow
        }
    }
    
    # Add some donations
    Write-Host "`n4. Adding sample donations..." -ForegroundColor Yellow
    
    $donations = @(
        @{ id = 1; amount = 0.3 },
        @{ id = 2; amount = 0.5 },
        @{ id = 3; amount = 0.8 }
    )
    
    foreach ($donation in $donations) {
        try {
            Invoke-RestMethod -Uri "$baseUrl/campaigns/$($donation.id)/donate" -Method POST -ContentType "application/json" -Body (@{
                amount = $donation.amount
            } | ConvertTo-Json) | Out-Null
            Write-Host "   ✅ Donated $($donation.amount) BTC to Campaign #$($donation.id)" -ForegroundColor Green
        } catch {
            Write-Host "   ⚠️  Could not donate to Campaign #$($donation.id)" -ForegroundColor Yellow
        }
    }
    
    Write-Host "`n✅ Demo data created successfully!" -ForegroundColor Green
}

function Clean-Database {
    Write-Section "Cleaning Database"
    
    $dbPath = "backend/data/openfunds.db"
    
    if (Test-Path $dbPath) {
        Write-Host "⚠️  This will delete all data!" -ForegroundColor Yellow
        $confirm = Read-Host "Are you sure? (yes/no)"
        
        if ($confirm -eq "yes") {
            Remove-Item $dbPath -Force
            Write-Host "✅ Database deleted" -ForegroundColor Green
            Write-Host "   Restart backend to create fresh database" -ForegroundColor Cyan
        } else {
            Write-Host "   Cancelled" -ForegroundColor Gray
        }
    } else {
        Write-Host "   No database found" -ForegroundColor Gray
    }
}

function Show-Menu {
    Write-Host "`n╔════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║   OpenFunds v2.0 - Demo Script        ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host "`nWhat would you like to do?`n" -ForegroundColor Yellow
    Write-Host "  1. Test Backend Connection" -ForegroundColor White
    Write-Host "  2. Show Platform Statistics" -ForegroundColor White
    Write-Host "  3. List All Campaigns" -ForegroundColor White
    Write-Host "  4. Create Demo Data" -ForegroundColor White
    Write-Host "  5. Clean Database" -ForegroundColor White
    Write-Host "  6. Full Demo (All above)" -ForegroundColor White
    Write-Host "  0. Exit" -ForegroundColor Gray
    Write-Host ""
}

# Main script logic
Clear-Host

if ($Clean) {
    Clean-Database
    exit
}

if ($ShowStats) {
    if (Test-Backend) {
        Show-Statistics
        Show-Campaigns
    }
    exit
}

if ($CreateDemoData) {
    if (Test-Backend) {
        Create-DemoData
        Show-Statistics
        Show-Campaigns
    }
    exit
}

# Interactive mode
while ($true) {
    Show-Menu
    $choice = Read-Host "Enter choice"
    
    switch ($choice) {
        "1" {
            Test-Backend
            Read-Host "`nPress Enter to continue"
        }
        "2" {
            if (Test-Backend) {
                Show-Statistics
            }
            Read-Host "`nPress Enter to continue"
        }
        "3" {
            if (Test-Backend) {
                Show-Campaigns
            }
            Read-Host "`nPress Enter to continue"
        }
        "4" {
            if (Test-Backend) {
                Create-DemoData
            }
            Read-Host "`nPress Enter to continue"
        }
        "5" {
            Clean-Database
            Read-Host "`nPress Enter to continue"
        }
        "6" {
            if (Test-Backend) {
                Show-Statistics
                Show-Campaigns
                $create = Read-Host "`nCreate demo data? (yes/no)"
                if ($create -eq "yes") {
                    Create-DemoData
                    Show-Statistics
                    Show-Campaigns
                }
            }
            Read-Host "`nPress Enter to continue"
        }
        "0" {
            Write-Host "`nGoodbye! 👋" -ForegroundColor Cyan
            exit
        }
        default {
            Write-Host "`n❌ Invalid choice. Please try again." -ForegroundColor Red
            Start-Sleep -Seconds 2
        }
    }
    
    Clear-Host
}
