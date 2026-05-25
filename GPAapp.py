from flask import Flask, render_template_string, request, jsonify
import json

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dự Đoán GPA</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            background: rgba(30, 30, 50, 0.9);
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 28px;
            background: linear-gradient(135deg, #00d4ff, #0099ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        h2 {
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #888;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .section {
            margin-bottom: 30px;
        }

        .input-group {
            margin-bottom: 25px;
        }

        .input-group label {
            display: block;
            font-size: 14px;
            margin-bottom: 10px;
            color: #b0b0b0;
            font-weight: 500;
        }

        .slider-container {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .slider {
            flex: 1;
            height: 6px;
            border-radius: 3px;
            background: rgba(255, 255, 255, 0.1);
            outline: none;
            -webkit-appearance: none;
            appearance: none;
            cursor: pointer;
        }

        .slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: linear-gradient(135deg, #00d4ff, #0099ff);
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0, 212, 255, 0.4);
            transition: all 0.2s;
        }

        .slider::-webkit-slider-thumb:hover {
            transform: scale(1.2);
            box-shadow: 0 4px 12px rgba(0, 212, 255, 0.6);
        }

        .slider::-moz-range-thumb {
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: linear-gradient(135deg, #00d4ff, #0099ff);
            cursor: pointer;
            border: none;
            box-shadow: 0 2px 8px rgba(0, 212, 255, 0.4);
            transition: all 0.2s;
        }

        .slider::-moz-range-thumb:hover {
            transform: scale(1.2);
            box-shadow: 0 4px 12px rgba(0, 212, 255, 0.6);
        }

        .slider-container span {
            min-width: 50px;
            text-align: right;
            font-weight: 600;
            color: #00d4ff;
            font-size: 14px;
        }

        .button-group {
            margin-bottom: 20px;
        }

        .button-group label {
            display: block;
            font-size: 14px;
            margin-bottom: 10px;
            color: #b0b0b0;
            font-weight: 500;
        }

        .button-options {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .btn-option {
            flex: 1;
            min-width: 100px;
            padding: 12px 20px;
            border: 2px solid rgba(255, 255, 255, 0.2);
            background: rgba(255, 255, 255, 0.05);
            color: #b0b0b0;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }

        .btn-option:hover {
            border-color: rgba(0, 212, 255, 0.5);
            color: #00d4ff;
        }

        .btn-option.active {
            background: linear-gradient(135deg, #00d4ff, #0099ff);
            border-color: #0099ff;
            color: #fff;
            box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
        }

        .result-section {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0, 153, 255, 0.1));
            border-radius: 12px;
            padding: 25px;
            margin-top: 40px;
            border: 1px solid rgba(0, 212, 255, 0.2);
        }

        .gpa-display {
            text-align: center;
            margin-bottom: 20px;
        }

        .gpa-label {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #888;
            margin-bottom: 10px;
        }

        .gpa-value {
            font-size: 56px;
            font-weight: 700;
            background: linear-gradient(135deg, #00d4ff, #0099ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 5px;
        }

        .gpa-scale {
            font-size: 14px;
            color: #666;
        }

        .gpa-details {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 8px;
            padding: 15px;
            font-size: 12px;
            line-height: 1.8;
            color: #a0a0a0;
        }

        .gpa-details p {
            margin-bottom: 8px;
        }

        .gpa-details strong {
            color: #00d4ff;
        }

        @media (max-width: 600px) {
            .container {
                padding: 20px;
            }
            
            h1 {
                font-size: 24px;
            }
            
            h2 {
                font-size: 12px;
            }
            
            .gpa-value {
                font-size: 48px;
            }
            
            .button-options {
                gap: 8px;
            }
            
            .btn-option {
                min-width: 80px;
                padding: 10px 15px;
                font-size: 12px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 Dự Đoán GPA</h1>
        
        <!-- THỜI GIAN & HỌC TẬP -->
        <div class="section">
            <h2>THỜI GIAN & HỌC TẬP</h2>
            
            <div class="input-group">
                <label>Số giờ học / tuần</label>
                <div class="slider-container">
                    <input type="range" id="studyHours" min="0" max="50" value="20" class="slider">
                    <span id="studyHoursValue">20</span> giờ
                </div>
            </div>
            
            <div class="input-group">
                <label>Số môn đang học</label>
                <div class="slider-container">
                    <input type="range" id="numSubjects" min="1" max="15" value="5" class="slider">
                    <span id="numSubjectsValue">5</span> môn
                </div>
            </div>
            
            <div class="input-group">
                <label>Tỷ lệ điểm danh trung bình (%)</label>
                <div class="slider-container">
                    <input type="range" id="attendanceRate" min="0" max="100" value="80" class="slider">
                    <span id="attendanceRateValue">80</span>%
                </div>
            </div>
        </div>
        
        <!-- SINH HOẠT HÀNG NGÀY -->
        <div class="section">
            <h2>SINH HOẠT HÀNG NGÀY</h2>
            
            <div class="input-group">
                <label>Thời gian ngủ / đêm (giờ)</label>
                <div class="slider-container">
                    <input type="range" id="sleepTime" min="0" max="12" step="0.5" value="7" class="slider">
                    <span id="sleepTimeValue">7</span> giờ
                </div>
            </div>
            
            <div class="input-group">
                <label>Thời gian mạng xã hội / ngày (giờ)</label>
                <div class="slider-container">
                    <input type="range" id="socialMediaTime" min="0" max="12" step="0.5" value="2" class="slider">
                    <span id="socialMediaTimeValue">2</span> giờ
                </div>
            </div>
        </div>
        
        <!-- HOẠT ĐỘNG KHÁC -->
        <div class="section">
            <h2>HOẠT ĐỘNG KHÁC</h2>
            
            <div class="button-group">
                <label>Làm thêm (part-time)?</label>
                <div class="button-options">
                    <button class="btn-option active" data-option="partTime" data-value="0">Không</button>
                    <button class="btn-option" data-option="partTime" data-value="1">Có</button>
                </div>
            </div>
            
            <div class="button-group">
                <label>Tham gia CLB?</label>
                <div class="button-options">
                    <button class="btn-option active" data-option="club" data-value="0">Không</button>
                    <button class="btn-option" data-option="club" data-value="1">Có</button>
                </div>
            </div>
            
            <div class="button-group">
                <label>Phương thức học</label>
                <div class="button-options">
                    <button class="btn-option active" data-option="studyMethod" data-value="0">Tự học</button>
                    <button class="btn-option" data-option="studyMethod" data-value="1">Học nhóm</button>
                    <button class="btn-option" data-option="studyMethod" data-value="2">Kết hợp</button>
                </div>
            </div>
        </div>
        
        <!-- KẾT QUẢ GPA -->
        <div class="section result-section">
            <h2>KẾT QUẢ</h2>
            <div class="gpa-display">
                <div class="gpa-label">GPA Dự Đoán</div>
                <div class="gpa-value" id="gpaValue">0.0</div>
                <div class="gpa-scale">/4.0</div>
            </div>
            <div class="gpa-details" id="gpaDetails"></div>
        </div>
    </div>
    
    <script>
        // Get all elements
        const studyHours = document.getElementById('studyHours');
        const numSubjects = document.getElementById('numSubjects');
        const attendanceRate = document.getElementById('attendanceRate');
        const sleepTime = document.getElementById('sleepTime');
        const socialMediaTime = document.getElementById('socialMediaTime');
        const gpaValue = document.getElementById('gpaValue');
        const gpaDetails = document.getElementById('gpaDetails');

        // Display values
        const studyHoursValue = document.getElementById('studyHoursValue');
        const numSubjectsValue = document.getElementById('numSubjectsValue');
        const attendanceRateValue = document.getElementById('attendanceRateValue');
        const sleepTimeValue = document.getElementById('sleepTimeValue');
        const socialMediaTimeValue = document.getElementById('socialMediaTimeValue');

        // Options state
        let options = {
            partTime: 0,
            club: 0,
            studyMethod: 0
        };

        // Update slider display values
        studyHours.addEventListener('input', (e) => {
            studyHoursValue.textContent = e.target.value;
            calculateGPA();
        });

        numSubjects.addEventListener('input', (e) => {
            numSubjectsValue.textContent = e.target.value;
            calculateGPA();
        });

        attendanceRate.addEventListener('input', (e) => {
            attendanceRateValue.textContent = e.target.value;
            calculateGPA();
        });

        sleepTime.addEventListener('input', (e) => {
            sleepTimeValue.textContent = e.target.value;
            calculateGPA();
        });

        socialMediaTime.addEventListener('input', (e) => {
            socialMediaTimeValue.textContent = e.target.value;
            calculateGPA();
        });

        // Button options
        document.querySelectorAll('.btn-option').forEach(btn => {
            btn.addEventListener('click', function() {
                const option = this.dataset.option;
                const value = parseInt(this.dataset.value);
                
                // Remove active from siblings
                document.querySelectorAll(`[data-option="${option}"]`).forEach(b => {
                    b.classList.remove('active');
                });
                
                // Add active to clicked
                this.classList.add('active');
                
                // Update options
                options[option] = value;
                calculateGPA();
            });
        });

        function calculateGPA() {
            const study = parseInt(studyHours.value);
            const subjects = parseInt(numSubjects.value);
            const attendance = parseInt(attendanceRate.value);
            const sleep = parseFloat(sleepTime.value);
            const socialMedia = parseFloat(socialMediaTime.value);
            const partTime = options.partTime;
            const club = options.club;
            const studyMethod = options.studyMethod;
            
            // Base GPA calculation
            let baseGPA = (attendance / 100) * 4.0;
            
            // Điều chỉnh GPA dựa trên tỷ lệ điểm danh và số môn
            if (subjects >= 12) {
                if (attendance < 65) {
                    baseGPA *= 0.90;
                } else if (attendance < 70) {
                    baseGPA *= 0.92;
                } else if (attendance < 80) {
                    baseGPA *= 0.98;
                }
            } else if (subjects >= 5) {
                if (attendance < 65) {
                    baseGPA *= 0.85;
                } else if (attendance < 70) {
                    baseGPA *= 0.90;
                } else if (attendance < 80) {
                    baseGPA *= 0.97;
                }
            } else {
                if (attendance < 65) {
                    baseGPA *= 0.80;
                } else if (attendance < 70) {
                    baseGPA *= 0.88;
                } else if (attendance < 80) {
                    baseGPA *= 0.96;
                }
            }
            
            // Apply modifiers
            let gpa = baseGPA;
            let details = [];
            
            details.push(`📚 Tỷ lệ điểm danh: ${attendance}%`);
            details.push(`📖 Số môn học: ${subjects}`);
            details.push(`⏱️ Giờ học/tuần: ${study}h`);
            
            // Sleep impact - ngủ quá ít thì GPA giảm
            let sleepMultiplier = 1.0;
            if (sleep < 5) {
                sleepMultiplier = 0.95;  // Giảm 5%
                details.push(`😴 Ngủ quá ít: ${sleep}h (Giảm 5%)`);
            } else if (sleep < 6) {
                sleepMultiplier = 0.97;
                details.push(`😴 Ngủ: ${sleep}h (Giảm 3%)`);
            } else if (sleep >= 6 && sleep <= 8) {
                sleepMultiplier = 1.0;
                details.push(`😴 Ngủ: ${sleep}h (Lý tưởng)`);
            } else if (sleep <= 9) {
                sleepMultiplier = 0.98;
                details.push(`😴 Ngủ: ${sleep}h (Hơi nhiều, giảm 2%)`);
            } else {
                sleepMultiplier = 0.95;
                details.push(`😴 Ngủ: ${sleep}h (Quá nhiều, giảm 5%)`);
            }
            
            gpa *= sleepMultiplier;
            
            // Social media impact - chơi nhiều thì GPA giảm
            let socialMultiplier = 1.0;
            if (socialMedia <= 1) {
                socialMultiplier = 1.05;  // Tăng 5%
                details.push(`📋 Mạng xã hội: ${socialMedia}h (Ít, tăng 5%)`);
            } else if (socialMedia <= 2) {
                socialMultiplier = 1.0;
                details.push(`📋 Mạng xã hội: ${socialMedia}h (Vừa phải)`);
            } else if (socialMedia <= 4) {
                socialMultiplier = 0.97;
                details.push(`📋 Mạng xã hội: ${socialMedia}h (Giảm 3%)`);
            } else {
                socialMultiplier = 0.90;
                details.push(`📋 Mạng xã hội: ${socialMedia}h (Nhiều, giảm 10%)`);
            }
            
            gpa *= socialMultiplier;
            
            // Study hours impact - đây là yếu tố CHÍNH
            let studyMultiplier = 1.0;
            if (study < 5) {
                studyMultiplier = 0.70;  // Giảm 30%
                details.push(`📚 Giờ học: ${study}h (Quá ít, giảm 30%)`);
            } else if (study < 10) {
                studyMultiplier = 0.85;  // Giảm 15%
                details.push(`📚 Giờ học: ${study}h (Ít, giảm 15%)`);
            } else if (study < 15) {
                studyMultiplier = 0.95;  // Giảm 5%
                details.push(`📚 Giờ học: ${study}h (Bình thường, giảm 5%)`);
            } else if (study < 20) {
                studyMultiplier = 1.0;   // Bình thường
                details.push(`📚 Giờ học: ${study}h (Tốt)`);
            } else if (study < 30) {
                studyMultiplier = 1.10;  // Tăng 10%
                details.push(`📚 Giờ học: ${study}h (Rất tốt, tăng 10%)`);
            } else if (study < 40) {
                studyMultiplier = 1.15;  // Tăng 15%
                details.push(`📚 Giờ học: ${study}h (Xuất sắc, tăng 15%)`);
            } else {
                studyMultiplier = 1.20;  // Tăng 20%
                details.push(`📚 Giờ học: ${study}h (Có thể quá nhiều, tăng 20%)`);
            }
            
            gpa *= studyMultiplier;
            
            // Study quality modifier based on study method
            let studyQuality = 1.0;
            if (studyMethod === 0) {
                studyQuality = 0.95;
                details.push(`📝 Phương thức: Tự học`);
            } else if (studyMethod === 1) {
                studyQuality = 1.05;
                details.push(`📝 Phương thức: Học nhóm (tốt)`);
            } else {
                studyQuality = 1.10;
                details.push(`📝 Phương thức: Kết hợp (tốt nhất)`);
            }
            
            gpa *= studyQuality;
            
            // Part-time work impact
            if (partTime === 1) {
                gpa *= 0.95;
                details.push(`💼 Làm thêm: Có (giảm 5%)`);
            }
            
            // Club participation impact
            if (club === 1) {
                gpa *= 0.95;
                details.push(`🎭 Tham gia CLB: Có (giảm 5%)`);
            }
            
            // Clamp GPA between 0 and 4.0
            gpa = Math.max(0, Math.min(4.0, gpa));
            
            // Display GPA
            gpaValue.textContent = gpa.toFixed(2);
            
            // Display details
            gpaDetails.innerHTML = details.map(d => `<p>${d}</p>`).join('');
            
            // Add recommendation
            let recommendation = '';
            if (gpa >= 3.7) {
                recommendation = '✨ Xuất sắc! Tiếp tục duy trì!';
            } else if (gpa >= 3.5) {
                recommendation = '🌟 Rất tốt! Hãy cố gắng thêm một chút!';
            } else if (gpa >= 3.0) {
                recommendation = '👍 Tốt! Cân bằng giữa học tập và cuộc sống.';
            } else if (gpa >= 2.5) {
                recommendation = '⚡ Cần cải thiện! Tăng thời gian học tập.';
            } else if (gpa >= 2.0) {
                recommendation = '⚠️ Cần nỗ lực hơn! Hãy đổ nhiều thời gian cho học tập.';
            } else {
                recommendation = '🔴 Tình trạng nguy hiểm! Cần thay đổi ngay!';
            }
            
            gpaDetails.innerHTML += `<p style="margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 15px;"><strong>${recommendation}</strong></p>`;
        }
        
        // Initial calculation
        calculateGPA();
    </script>
</body>
</html>
'''

def calculate_gpa(study_hours, num_subjects, attendance_rate, sleep_time, social_media_time, part_time, club, study_method):
    """Calculate GPA based on input parameters"""
    
    # Base GPA calculation
    base_gpa = (attendance_rate / 100) * 4.0
    
    # Điều chỉnh GPA dựa trên tỷ lệ điểm danh và số môn
    if num_subjects >= 12:
        if attendance_rate < 65:
            base_gpa *= 0.90
        elif attendance_rate < 70:
            base_gpa *= 0.92
        elif attendance_rate < 80:
            base_gpa *= 0.98
    elif num_subjects >= 5:
        if attendance_rate < 65:
            base_gpa *= 0.85
        elif attendance_rate < 70:
            base_gpa *= 0.90
        elif attendance_rate < 80:
            base_gpa *= 0.97
    else:
        if attendance_rate < 65:
            base_gpa *= 0.80
        elif attendance_rate < 70:
            base_gpa *= 0.88
        elif attendance_rate < 80:
            base_gpa *= 0.96
    
    gpa = base_gpa
    details = []
    
    details.append(f"📚 Tỷ lệ điểm danh: {attendance_rate}%")
    details.append(f"📖 Số môn học: {num_subjects}")
    details.append(f"⏱️ Giờ học/tuần: {study_hours}h")
    
    # Sleep impact - ngủ quá ít thì GPA giảm
    sleep_multiplier = 1.0
    if sleep_time < 5:
        sleep_multiplier = 0.95
        details.append(f"😴 Ngủ quá ít: {sleep_time}h (Giảm 5%)")
    elif sleep_time < 6:
        sleep_multiplier = 0.97
        details.append(f"😴 Ngủ: {sleep_time}h (Giảm 3%)")
    elif sleep_time >= 6 and sleep_time <= 8:
        sleep_multiplier = 1.0
        details.append(f"😴 Ngủ: {sleep_time}h (Lý tưởng)")
    elif sleep_time <= 9:
        sleep_multiplier = 0.98
        details.append(f"😴 Ngủ: {sleep_time}h (Hơi nhiều, giảm 2%)")
    else:
        sleep_multiplier = 0.95
        details.append(f"😴 Ngủ: {sleep_time}h (Quá nhiều, giảm 5%)")
    
    gpa *= sleep_multiplier
    
    # Social media impact - chơi nhiều thì GPA giảm
    social_multiplier = 1.0
    if social_media_time <= 1:
        social_multiplier = 1.05
        details.append(f"📋 Mạng xã hội: {social_media_time}h (Ít, tăng 5%)")
    elif social_media_time <= 2:
        social_multiplier = 1.0
        details.append(f"📋 Mạng xã hội: {social_media_time}h (Vừa phải)")
    elif social_media_time <= 4:
        social_multiplier = 0.97
        details.append(f"📋 Mạng xã hội: {social_media_time}h (Giảm 3%)")
    else:
        social_multiplier = 0.90
        details.append(f"📋 Mạng xã hội: {social_media_time}h (Nhiều, giảm 10%)")
    
    gpa *= social_multiplier
    
    # Study hours impact - đây là yếu tố CHÍNH
    study_multiplier = 1.0
    if study_hours < 5:
        study_multiplier = 0.70
        details.append(f"📚 Giờ học: {study_hours}h (Quá ít, giảm 30%)")
    elif study_hours < 10:
        study_multiplier = 0.85
        details.append(f"📚 Giờ học: {study_hours}h (Ít, giảm 15%)")
    elif study_hours < 15:
        study_multiplier = 0.95
        details.append(f"📚 Giờ học: {study_hours}h (Bình thường, giảm 5%)")
    elif study_hours < 20:
        study_multiplier = 1.0
        details.append(f"📚 Giờ học: {study_hours}h (Tốt)")
    elif study_hours < 30:
        study_multiplier = 1.10
        details.append(f"📚 Giờ học: {study_hours}h (Rất tốt, tăng 10%)")
    elif study_hours < 40:
        study_multiplier = 1.15
        details.append(f"📚 Giờ học: {study_hours}h (Xuất sắc, tăng 15%)")
    else:
        study_multiplier = 1.20
        details.append(f"📚 Giờ học: {study_hours}h (Có thể quá nhiều, tăng 20%)")
    
    gpa *= study_multiplier
    
    # Study quality modifier
    study_quality = 1.0
    if study_method == 0:
        study_quality = 0.95
        details.append("📝 Phương thức: Tự học")
    elif study_method == 1:
        study_quality = 1.05
        details.append("📝 Phương thức: Học nhóm (tốt)")
    else:
        study_quality = 1.10
        details.append("📝 Phương thức: Kết hợp (tốt nhất)")
    
    gpa *= study_quality
    
    # Part-time work impact
    if part_time == 1:
        gpa *= 0.95
        details.append("💼 Làm thêm: Có (giảm 5%)")
    
    # Club participation impact
    if club == 1:
        gpa *= 0.95
        details.append("🎭 Tham gia CLB: Có (giảm 5%)")
    
    # Clamp GPA between 0 and 4.0
    gpa = max(0, min(4.0, gpa))
    
    # Recommendation
    if gpa >= 3.7:
        recommendation = "✨ Xuất sắc! Tiếp tục duy trì!"
    elif gpa >= 3.5:
        recommendation = "🌟 Rất tốt! Hãy cố gắng thêm một chút!"
    elif gpa >= 3.0:
        recommendation = "👍 Tốt! Cân bằng giữa học tập và cuộc sống."
    elif gpa >= 2.5:
        recommendation = "⚡ Cần cải thiện! Tăng thời gian học tập."
    elif gpa >= 2.0:
        recommendation = "⚠️ Cần nỗ lực hơn! Hãy đổ nhiều thời gian cho học tập."
    else:
        recommendation = "🔴 Tình trạng nguy hiểm! Cần thay đổi ngay!"
    
    details.append(f"\n{recommendation}")
    
    return gpa, details

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    data = request.json
    gpa, details = calculate_gpa(
        study_hours=data.get('studyHours', 20),
        num_subjects=data.get('numSubjects', 5),
        attendance_rate=data.get('attendanceRate', 80),
        sleep_time=data.get('sleepTime', 7),
        social_media_time=data.get('socialMediaTime', 2),
        part_time=data.get('partTime', 0),
        club=data.get('club', 0),
        study_method=data.get('studyMethod', 0)
    )
    
    return jsonify({
        'gpa': round(gpa, 2),
        'details': details
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
