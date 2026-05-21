/**
 * STDD Playground — Stepper engine
 * Data-driven phase renderer with Gate interaction and scroll control.
 * Zero dependencies. Uses IntersectionObserver and standard DOM APIs.
 */

const Stepper = (function() {
    'use strict';

    let container = null;
    let data = null;
    let gateStates = {};
    let observer = null;

    const STORAGE_KEY_PREFIX = 'stdd_pg_gate_';

    function init(containerId, scenarioData) {
        container = document.getElementById(containerId);
        data = scenarioData;
        if (!container || !data) {
            console.error('Stepper: missing container or scenario data');
            return;
        }
        loadGateStates();
        render();
        setupObserver();
    }

    function loadGateStates() {
        try {
            const key = STORAGE_KEY_PREFIX + data.title.replace(/\s+/g, '_').toLowerCase();
            const saved = sessionStorage.getItem(key);
            gateStates = saved ? JSON.parse(saved) : {};
        } catch (e) {
            gateStates = {};
        }
    }

    function saveGateStates() {
        try {
            const key = STORAGE_KEY_PREFIX + data.title.replace(/\s+/g, '_').toLowerCase();
            sessionStorage.setItem(key, JSON.stringify(gateStates));
        } catch (e) { /* ignore */ }
    }

    function isGatePassed(gateId) {
        return !!gateStates[gateId];
    }

    function setGatePassed(gateId) {
        gateStates[gateId] = true;
        saveGateStates();
    }

    function render() {
        if (!data.phases || data.phases.length === 0) return;

        // Hero section
        const hero = document.createElement('div');
        hero.className = 'pg-hero';
        hero.innerHTML = '<h1>' + escapeHtml(data.title) + '</h1>' +
            (data.subtitle ? '<p class="pg-hero-sub">' + escapeHtml(data.subtitle) + '</p>' : '');
        container.appendChild(hero);

        // Phase sections
        data.phases.forEach(function(phase, idx) {
            renderPhase(phase, idx);
        });

        // CTA section
        if (data.cta) {
            renderCta(data.cta);
        }
    }

    function renderPhase(phase, idx) {
        const el = document.createElement('section');
        el.className = 'pg-phase';
        el.id = 'phase-' + phase.id;
        if (idx > 0) {
            el.classList.add('pg-phase--dimmed');
        }

        // Phase header
        const header = document.createElement('div');
        header.className = 'pg-phase-header';
        header.innerHTML = '<span class="pg-phase-num">Phase ' + (idx + 1) + '</span>' +
            '<h2>' + escapeHtml(phase.title) + '</h2>';
        el.appendChild(header);

        // Phase content sections
        if (phase.sections) {
            phase.sections.forEach(function(sec) {
                el.appendChild(renderSection(sec));
            });
        }

        // Gate (if present)
        if (phase.gate) {
            el.appendChild(renderGate(phase.gate, idx));
        }

        container.appendChild(el);
    }

    function renderSection(sec) {
        const wrapper = document.createElement('div');
        wrapper.className = 'pg-section';

        switch (sec.type) {
            case 'input':
                wrapper.className += ' pg-input-block';
                wrapper.innerHTML = '<div class="terminal">' +
                    '<span class="prompt dollar"></span>' +
                    '<span class="command">' + escapeHtml(sec.content) + '</span>' +
                    '<span class="cursor"></span>' +
                    '</div>';
                break;

            case 'markdown':
                wrapper.className += ' pg-md-block';
                if (sec.title) {
                    const h = document.createElement('h3');
                    h.textContent = sec.title;
                    wrapper.appendChild(h);
                }
                const md = document.createElement('div');
                md.className = 'pg-md-content';
                md.innerHTML = sec.content;
                wrapper.appendChild(md);
                break;

            case 'code':
                wrapper.className += ' pg-code-block';
                if (sec.title) {
                    const h = document.createElement('h4');
                    h.textContent = sec.title;
                    wrapper.appendChild(h);
                }
                const pre = document.createElement('pre');
                const code = document.createElement('code');
                if (sec.language) {
                    code.className = 'language-' + sec.language;
                }
                code.textContent = sec.content;
                pre.appendChild(code);
                wrapper.appendChild(pre);
                // Trigger Prism highlighting if available
                if (typeof Prism !== 'undefined' && Prism.highlightElement) {
                    Prism.highlightElement(code);
                }
                break;

            case 'table':
                wrapper.className += ' pg-table-block';
                if (sec.title) {
                    const h = document.createElement('h4');
                    h.textContent = sec.title;
                    wrapper.appendChild(h);
                }
                const table = document.createElement('table');
                table.className = 'pg-table';
                if (sec.headers) {
                    const thead = document.createElement('thead');
                    const tr = document.createElement('tr');
                    sec.headers.forEach(function(h) {
                        const th = document.createElement('th');
                        th.textContent = h;
                        tr.appendChild(th);
                    });
                    thead.appendChild(tr);
                    table.appendChild(thead);
                }
                if (sec.rows) {
                    const tbody = document.createElement('tbody');
                    sec.rows.forEach(function(row) {
                        const tr = document.createElement('tr');
                        row.forEach(function(cell) {
                            const td = document.createElement('td');
                            td.innerHTML = cell;
                            tr.appendChild(td);
                        });
                        tbody.appendChild(tr);
                    });
                    table.appendChild(tbody);
                }
                wrapper.appendChild(table);
                break;

            case 'split-view':
                wrapper.className += ' pg-split-view';
                const left = document.createElement('div');
                left.className = 'pg-split-left';
                left.textContent = sec.left || '';
                wrapper.appendChild(left);
                const arrow = document.createElement('div');
                arrow.className = 'pg-split-arrow';
                arrow.textContent = '→';
                wrapper.appendChild(arrow);
                const right = document.createElement('div');
                right.className = 'pg-split-right';
                right.textContent = sec.right || '';
                wrapper.appendChild(right);
                break;

            case 'cards':
                wrapper.className += ' pg-cards-grid';
                if (sec.items) {
                    sec.items.forEach(function(card) {
                        const cardEl = document.createElement('div');
                        cardEl.className = 'pg-card';
                        cardEl.innerHTML = (card.icon ? '<span class="pg-card-icon">' + escapeHtml(card.icon) + '</span>' : '') +
                            '<strong>' + escapeHtml(card.label || '') + '</strong>' +
                            '<p>' + escapeHtml(card.desc || '') + '</p>';
                        wrapper.appendChild(cardEl);
                    });
                }
                break;

            case 'animation':
                wrapper.className += ' pg-anim-block';
                wrapper.setAttribute('data-anim', sec.animType || 'typewriter');
                wrapper.innerHTML = '<div class="pg-anim-content">' + escapeHtml(sec.content || '') + '</div>';
                break;

            default:
                wrapper.textContent = sec.content || '';
        }

        return wrapper;
    }

    function renderGate(gate, phaseIdx) {
        const el = document.createElement('div');
        const gateNum = phaseIdx <= 1 ? (phaseIdx + 1) : (phaseIdx === 4 ? 3 : 2);
        // Map: Phase 1→Gate1, Phase 2→Gate2, Phase 5→Gate3

        let gateClass = 'gate gate-' + gateNum;
        if (isGatePassed(gate.id)) {
            gateClass += ' passed';
        }

        el.className = gateClass;
        el.id = 'gate-' + gate.id;

        const iconMap = {1: '🔒', 2: '⭐', 3: '🏁'};
        const labelMap = {1: 'Gate 1：确认 scope / 边界 / 成功标准', 2: 'Gate 2：确认设计基线（最关键的分水岭）', 3: 'Gate 3：质量终审'};

        el.innerHTML = '<div class="gate-header">' +
            '<span class="gate-icon">' + (iconMap[gateNum] || '🔒') + '</span>' +
            escapeHtml(labelMap[gateNum] || '') +
            '</div>';

        const interact = document.createElement('div');
        interact.className = 'gate-interact';

        if (isGatePassed(gate.id)) {
            interact.innerHTML = '<p style="color:#009573;font-weight:500;">✓ 已确认</p>';
        } else if (gate.type === 'checkbox' && gate.items) {
            const list = document.createElement('ul');
            list.className = 'gate-checklist';
            gate.items.forEach(function(item, i) {
                const li = document.createElement('li');
                li.textContent = item;
                li.addEventListener('click', function() {
                    li.classList.toggle('checked');
                    checkAllChecked(list, gate);
                });
                list.appendChild(li);
            });
            interact.appendChild(list);

            const btn = document.createElement('button');
            btn.className = 'gate-btn';
            btn.textContent = gate.buttonText || '确认 Proposal → 进入 Phase 2';
            btn.disabled = true;
            btn.addEventListener('click', function() {
                setGatePassed(gate.id);
                refreshGate(el, gate);
                activateNextPhase(phaseIdx);
            });
            interact.appendChild(btn);

        } else if (gate.type === 'button') {
            const btn = document.createElement('button');
            btn.className = 'gate-btn';
            btn.textContent = gate.buttonText || '确认设计基线，进入自动执行';
            btn.addEventListener('click', function() {
                setGatePassed(gate.id);
                refreshGate(el, gate);
                activateNextPhases(phaseIdx);
            });
            interact.appendChild(btn);
        }

        el.appendChild(interact);
        return el;
    }

    function checkAllChecked(listEl, gate) {
        const items = listEl.querySelectorAll('li');
        const allChecked = Array.from(items).every(function(li) { return li.classList.contains('checked'); });
        const btn = listEl.parentElement.querySelector('.gate-btn');
        if (btn) {
            btn.disabled = !allChecked;
        }
    }

    function refreshGate(el, gate) {
        el.classList.add('passed');
        const interact = el.querySelector('.gate-interact');
        if (interact) {
            interact.innerHTML = '<p style="color:#009573;font-weight:500;">✓ 已确认</p>';
        }
    }

    function activateNextPhase(currentIdx) {
        const next = container.querySelector('#phase-' + data.phases[Math.min(currentIdx + 1, data.phases.length - 1)].id);
        if (next) {
            next.classList.remove('pg-phase--dimmed');
            setTimeout(function() {
                next.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 200);
        }
    }

    function activateNextPhases(currentIdx) {
        // Activate all remaining phases (for Gate 2 → auto-run Phase 3-5)
        var allPhases = container.querySelectorAll('.pg-phase');
        allPhases.forEach(function(ph, i) {
            if (i > currentIdx) {
                ph.classList.remove('pg-phase--dimmed');
            }
        });
        const next = container.querySelector('#phase-' + data.phases[Math.min(currentIdx + 1, data.phases.length - 1)].id);
        if (next) {
            setTimeout(function() {
                next.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 200);
        }
    }

    function setupObserver() {
        if (typeof IntersectionObserver === 'undefined') {
            // Fallback: show all phases
            container.querySelectorAll('.pg-phase--dimmed').forEach(function(el) {
                el.classList.remove('pg-phase--dimmed');
            });
            return;
        }

        observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.remove('pg-phase--dimmed');
                }
            });
        }, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

        container.querySelectorAll('.pg-phase--dimmed').forEach(function(el) {
            observer.observe(el);
        });
    }

    function renderCta(cta) {
        const el = document.createElement('section');
        el.className = 'pg-cta';
        el.innerHTML = '<h2>' + escapeHtml(cta.text || '用 STDD 管理你的下一个需求') + '</h2>';

        if (cta.commands) {
            const cmdBox = document.createElement('div');
            cmdBox.className = 'terminal';
            cmdBox.style.maxWidth = '600px';
            cmdBox.style.margin = '16px auto';
            cmdBox.innerHTML = cta.commands.map(function(c) {
                return '<span class="prompt dollar"></span><span class="command">' + escapeHtml(c) + '</span>';
            }).join('<br>');
            el.appendChild(cmdBox);
        }

        const btns = document.createElement('div');
        btns.className = 'pg-cta-btns';

        if (cta.copyTarget) {
            const copyBtn = document.createElement('button');
            copyBtn.className = 'gate-btn';
            copyBtn.textContent = '📋 复制安装命令';
            copyBtn.addEventListener('click', function() {
                var text = cta.commands ? cta.commands.join('\n') : '';
                navigator.clipboard.writeText(text).then(function() {
                    copyBtn.textContent = '✓ 已复制';
                    copyBtn.style.background = '#009573';
                    setTimeout(function() {
                        copyBtn.textContent = '📋 复制安装命令';
                        copyBtn.style.background = '';
                    }, 2000);
                }).catch(function() {
                    copyBtn.textContent = '⚠ 复制失败，请手动选择';
                });
            });
            btns.appendChild(copyBtn);
        }

        if (cta.tutorialUrl) {
            const tutBtn = document.createElement('a');
            tutBtn.className = 'gate-btn';
            tutBtn.style.background = 'transparent';
            tutBtn.style.color = '#009573';
            tutBtn.style.border = '1.5px solid #009573';
            tutBtn.style.marginLeft = '12px';
            tutBtn.href = cta.tutorialUrl;
            tutBtn.textContent = '📖 查看完整教程';
            btns.appendChild(tutBtn);
        }

        el.appendChild(btns);
        container.appendChild(el);
    }

    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    return { init: init };
})();
