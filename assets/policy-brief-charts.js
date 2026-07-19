/**
 * Policy brief charts — Chart.js 의존 (CDN). 난독화 제외, 미니파이만 적용.
 */
(function () {
  function boot() {
    if (typeof Chart === 'undefined') {
      setTimeout(boot, 40);
      return;
    }

    const ORANGE = '#ff751b';
    const BLUE = '#4169e1';
    const INK = '#172033';
    const RED = '#c44a3a';
    const MUTED = '#667085';
    const LINE = '#e3e8f2';

    Chart.defaults.font.family = 'Pretendard, "Noto Sans KR", "Apple SD Gothic Neo", system-ui, sans-serif';
    Chart.defaults.color = MUTED;

    const crime = document.getElementById('chartCrime');
    if (crime) {
      new Chart(crime, {
        type: 'bar',
        data: {
          labels: ['2020', '2021', '2022', '2023', '2024'],
          datasets: [{
            label: '국내체류 외국인 피의자 수',
            data: [null, null, null, 33052, 35296],
            backgroundColor: BLUE,
            borderRadius: 6,
            maxBarThickness: 56
          }]
        },
        options: {
          plugins: {
            legend: { display: false },
            title: { display: true, text: '국내체류 외국인 피의자 수 (명)', color: INK, font: { size: 13, weight: '700' } }
          },
          scales: {
            y: { beginAtZero: true, grid: { color: LINE } },
            x: { grid: { display: false } }
          }
        }
      });
    }

    const undoc = document.getElementById('chartUndoc');
    if (undoc) {
      new Chart(undoc, {
        type: 'doughnut',
        data: {
          labels: ['불법체류 외국인 (13%)', '합법 체류 외국인 (87%)'],
          datasets: [{
            data: [13, 87],
            backgroundColor: [RED, '#dce3f0'],
            borderWidth: 0
          }]
        },
        options: {
          cutout: '68%',
          plugins: {
            legend: { position: 'bottom' },
            title: { display: true, text: '2026.1 기준 체류외국인 중 불법체류 비중', color: INK, font: { size: 13, weight: '700' } }
          }
        }
      });
    }

    const accident = document.getElementById('chartAccident');
    if (accident) {
      new Chart(accident, {
        type: 'bar',
        data: {
          labels: ['2020', '2021', '2022', '2023', '2024', '2025(상반기)'],
          datasets: [{
            label: '외국인 근로자 산재 피해 인원 (명)',
            data: [7583, null, null, null, 9219, 4550],
            backgroundColor: (ctx) => (ctx.dataIndex === 5 ? ORANGE : BLUE),
            borderRadius: 6,
            maxBarThickness: 52
          }]
        },
        options: {
          plugins: {
            legend: { display: false },
            title: { display: true, text: '연도별 외국인 근로자 산재 피해 인원', color: INK, font: { size: 13, weight: '700' } }
          },
          scales: {
            y: { beginAtZero: true, grid: { color: LINE } },
            x: { grid: { display: false } }
          }
        }
      });
    }

    const wage = document.getElementById('chartWage');
    if (wage) {
      new Chart(wage, {
        type: 'line',
        data: {
          labels: ['2023', '2024', '2025.7'],
          datasets: [{
            label: '1인당 평균 임금체불 피해액(만원)',
            data: [447, 476, 503],
            borderColor: RED,
            backgroundColor: 'rgba(196,74,58,0.12)',
            fill: true,
            tension: 0.3,
            pointBackgroundColor: RED,
            pointRadius: 5
          }]
        },
        options: {
          plugins: {
            legend: { display: false },
            title: { display: true, text: '외국인 근로자 임금체불 평균 피해액 추이', color: INK, font: { size: 13, weight: '700' } }
          },
          scales: {
            y: { grid: { color: LINE }, ticks: { callback: (v) => v + '만원' } },
            x: { grid: { display: false } }
          }
        }
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
