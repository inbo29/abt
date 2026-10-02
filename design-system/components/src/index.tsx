// ABT Ops — components. React 18 comes from window.React; this file builds to ONE classic
// script that assigns window.Abt. Icons appear only in menus (SideNav, MobileTabBar) and as
// a few functional glyphs (select chevron, sort caret). Colour is reserved for status.
import { ICONS } from './icons';

const R: any = (window as any).React;
const React = R;
const { useState, useId } = R;

const cx = (...a: any[]) => a.filter(Boolean).join(' ');

/* ------------------------------------------------------------------ formatting */

export const CURRENCIES: Record<string, { digits: number }> = {
  KRW: { digits: 0 },
  USD: { digits: 2 },
  MNT: { digits: 0 },
};

export function formatNumber(n: number, digits = 0) {
  return new Intl.NumberFormat('ko-KR', { minimumFractionDigits: digits, maximumFractionDigits: digits }).format(Math.abs(n));
}

/** Korean compact units for KPI tiles: 48,200,000 → 4,820만 · 1,240,000,000 → 12.4억 */
export function formatCompact(n: number) {
  const a = Math.abs(n);
  if (a >= 1e8) {
    const v = a / 1e8;
    return (v >= 10 ? v.toFixed(1) : v.toFixed(2)).replace(/\.?0+$/, '') + '억';
  }
  if (a >= 1e4) return formatNumber(Math.round(a / 1e4)) + '만';
  return formatNumber(a);
}

export function formatMoney(amount: number, currency = 'KRW', opts: any = {}) {
  const digits = CURRENCIES[currency]?.digits ?? 0;
  const neg = amount < 0;
  const sign = neg ? '−' : opts.sign === 'always' && amount > 0 ? '+' : '';
  const num = opts.compact ? formatCompact(amount) : formatNumber(amount, digits);
  return sign + num;
}

/* ------------------------------------------------------------------ Icon */

export function Icon({ name, size = 18, strokeWidth = 1.75, title, className, style }: any) {
  const els = ICONS[name];
  if (!els) return null;
  return (
    <svg
      className={cx('abt-icon', className)}
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
      role={title ? 'img' : undefined}
      aria-hidden={title ? undefined : true}
      aria-label={title}
      focusable="false"
      style={style}
    >
      {els.map(([tag, attrs]: any, i: number) => React.createElement(tag, { key: i, ...attrs }))}
    </svg>
  );
}

/* ------------------------------------------------------------------ Button */

export function Button({ variant = 'secondary', size = 'md', href, block, disabled, type = 'button', className, children, ...rest }: any) {
  const cls = cx('abt-btn', `abt-btn--${variant}`, `abt-btn--${size}`, block && 'abt-btn--block', className);
  if (href && !disabled) {
    return (
      <a className={cls} href={href} {...rest}>
        {children}
      </a>
    );
  }
  return (
    <button type={type} className={cls} disabled={disabled} {...rest}>
      {children}
    </button>
  );
}

/* ------------------------------------------------------------------ StatusBadge */

const S = (label: string, tone: string, form = 'solid') => ({ label, tone, form });

/** The fixed status vocabulary: one word per state, per axis. form: solid | dashed (provisional) | strong (act now). */
export const STATUS: Record<string, Record<string, { label: string; tone: string; form: string }>> = {
  event: {
    booked: S('예약', 'neutral', 'dashed'),
    confirmed: S('확정', 'neutral'),
    'in-progress': S('진행 중', 'progress', 'strong'),
    completed: S('완료', 'neutral'),
    cancelled: S('취소', 'neutral'),
  },
  cost: {
    draft: S('임시저장', 'neutral', 'dashed'),
    submitted: S('제출', 'progress', 'dashed'),
    reviewing: S('검토 중', 'progress', 'dashed'),
    supplement: S('보완 요청', 'attention'),
    approved: S('승인', 'positive'),
    rejected: S('반려', 'critical'),
  },
  remit: {
    requested: S('요청', 'progress', 'dashed'),
    reviewing: S('검토 중', 'progress', 'dashed'),
    approved: S('승인', 'positive', 'dashed'),
    partial: S('일부 송금', 'progress'),
    completed: S('송금 완료', 'positive'),
    rejected: S('반려', 'critical'),
  },
  payment: {
    billed: S('청구', 'neutral', 'dashed'),
    partial: S('부분 입금', 'progress'),
    paid: S('입금 완료', 'positive'),
    'due-soon': S('기한 임박', 'attention'),
    overdue: S('연체', 'critical'),
  },
  settle: {
    open: S('미정산', 'neutral', 'dashed'),
    reviewing: S('정산 검토', 'progress', 'dashed'),
    settled: S('정산 확정', 'positive'),
    closed: S('마감', 'neutral'),
    reopened: S('재개방', 'attention'),
  },
  assign: {
    unassigned: S('미배정', 'attention'),
    tentative: S('가배정', 'neutral', 'dashed'),
    confirmed: S('배정 확정', 'neutral'),
    changed: S('변경 확인 필요', 'attention'),
    acknowledged: S('가이드 확인', 'positive'),
    conflict: S('일정 충돌', 'critical'),
  },
  claim: {
    received: S('접수', 'attention'),
    investigating: S('조사 중', 'progress'),
    acting: S('조치 중', 'progress'),
    resolved: S('해결 확인', 'positive'),
    closed: S('종결', 'neutral'),
    overdue: S('기한 초과', 'critical'),
    urgent: S('긴급', 'critical', 'strong'),
  },
  report: {
    draft: S('작성 중', 'neutral', 'dashed'),
    submitted: S('제출', 'progress', 'dashed'),
    confirmed: S('확인 완료', 'positive'),
  },
  risk: {
    overrun: S('예산 초과', 'attention'),
    'missing-proof': S('증빙 누락', 'attention'),
    duplicate: S('중복 청구 후보', 'attention'),
    'rate-diff': S('단가 차이', 'attention'),
    'margin-drop': S('마진 하락', 'attention'),
    repeat: S('반복 클레임', 'attention'),
    deficit: S('적자', 'critical'),
    overdue: S('미수 기한 경과', 'critical'),
    'claim-delay': S('처리 기한 초과', 'critical'),
  },
};

export function statusLabel(axis: string, status: string) {
  return STATUS[axis]?.[status]?.label ?? status;
}

export function StatusBadge({ axis, status, tone, form, size = 'sm', children, title }: any) {
  const def = axis && status ? STATUS[axis]?.[status] : null;
  const t = tone || def?.tone || 'neutral';
  const f = form || def?.form || 'solid';
  const label = children ?? def?.label ?? status;
  return (
    <span className={cx('abt-badge', `abt-badge--${t}`, `abt-badge--${f}`, `abt-badge--${size}`)} title={title}>
      {label}
    </span>
  );
}

/* ------------------------------------------------------------------ Money */

export function Money({ amount, currency = 'KRW', kind = 'actual', converted, rate, size = 'md', sign, compact, tag, lossTone, align = 'end' }: any) {
  if (amount == null || amount === '') return <span className="abt-muted">—</span>;
  const n = Number(amount);
  const expected = kind === 'expected';
  const loss = lossTone && n < 0;
  return (
    <span
      className={cx('abt-money', `abt-money--${size}`, `abt-money--${align}`, expected && 'is-expected', loss && 'is-loss')}
      title={expected ? '예상 금액' : undefined}
    >
      <span className="abt-money__main">
        {tag && expected && <span className="abt-money__tag">예상</span>}
        <span className="abt-money__num">{formatMoney(n, currency, { sign, compact })}</span>
        <span className="abt-money__cur">{currency}</span>
        {expected && !tag && <span className="abt-sr">(예상)</span>}
      </span>
      {converted && (
        <span className="abt-money__conv">
          ≈ {formatMoney(Number(converted.amount), converted.currency)} {converted.currency}
          {rate && (
            <>
              {' '}
              · {rate.value}
              {rate.date ? ` (${rate.date})` : ''}
            </>
          )}
        </span>
      )}
    </span>
  );
}

/* ------------------------------------------------------------------ EventCode */

export function EventCode({ code, href, size = 'sm', title }: any) {
  const Tag: any = href ? 'a' : 'span';
  return (
    <Tag className={cx('abt-code', `abt-code--${size}`, href && 'is-link')} href={href} title={title}>
      {code}
    </Tag>
  );
}

/* ------------------------------------------------------------------ DateTime */

const ZONES: Record<string, number> = { KST: 9, ULAT: 8 };
const DOW = ['일', '월', '화', '수', '목', '금', '토'];
const pad = (n: number) => String(n).padStart(2, '0');

function parseLocal(value: string) {
  const m = /^(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2}))?/.exec(value || '');
  if (!m) return null;
  return { y: +m[1], mo: +m[2], d: +m[3], h: m[4] != null ? +m[4] : null, mi: m[5] != null ? +m[5] : null };
}

/** value: "2026-10-01T14:30" in the given zone (KST | ULAT). */
export function DateTime({ value, zone = 'ULAT', format = 'datetime', other, showZone = true }: any) {
  const p = parseLocal(value);
  if (!p) return <span className="abt-dt">{value}</span>;
  const dow = DOW[new Date(Date.UTC(p.y, p.mo - 1, p.d)).getUTCDay()];
  const dateFull = `${p.y}.${pad(p.mo)}.${pad(p.d)} (${dow})`;
  const dateShort = `${pad(p.mo)}.${pad(p.d)}(${dow})`;
  const time = p.h != null ? `${pad(p.h)}:${pad(p.mi as number)}` : '';
  let main = dateShort;
  if (format === 'date') main = dateFull;
  if (format === 'datetime') main = time ? `${dateShort} ${time}` : dateShort;
  if (format === 'time') main = time;
  const hasTime = (format === 'datetime' || format === 'time') && !!time;
  let otherStr: string | null = null;
  if (other && p.h != null) {
    const oz = other === true ? (zone === 'KST' ? 'ULAT' : 'KST') : other;
    const diff = (ZONES[oz] ?? 0) - (ZONES[zone] ?? 0);
    const t = new Date(Date.UTC(p.y, p.mo - 1, p.d, p.h + diff, p.mi as number));
    otherStr = `${pad(t.getUTCHours())}:${pad(t.getUTCMinutes())} ${oz}` + (t.getUTCDate() !== p.d ? ` (${pad(t.getUTCMonth() + 1)}.${pad(t.getUTCDate())})` : '');
  }
  return (
    <time className="abt-dt" dateTime={value}>
      {main}
      {hasTime && showZone && <span className="abt-dt__zone">{zone}</span>}
      {otherStr && <span className="abt-dt__other">{otherStr}</span>}
    </time>
  );
}

/* ------------------------------------------------------------------ KpiTile */

export function KpiTile({ label, value, unit, money, delta, state, stateLabel, caption, href, linkLabel = '원장 보기' }: any) {
  let deltaNode = null;
  if (delta && delta.value != null) {
    const v = Number(delta.value);
    const up = v > 0;
    const down = v < 0;
    const bad = (delta.good === 'up' && down) || (delta.good === 'down' && up);
    const sign = up ? '+' : down ? '−' : '±';
    const digits = delta.digits ?? (Number.isInteger(v) ? 0 : 1);
    deltaNode = (
      <span className={cx('abt-kpi__delta', bad && 'is-bad')}>
        {sign}
        {formatNumber(Math.abs(v), digits)}
        {delta.unit ?? '%'}
        {delta.period ? <span className="abt-kpi__period"> {delta.period}</span> : null}
      </span>
    );
  }
  return (
    <div className={cx('abt-kpi', state && `abt-kpi--${state}`)}>
      <div className="abt-kpi__head">
        <span className="abt-kpi__label">{label}</span>
        {stateLabel && <span className="abt-kpi__state">{stateLabel}</span>}
      </div>
      <div className="abt-kpi__value">
        {money ? (
          <Money size="kpi" align="start" compact={money.compact ?? true} {...money} />
        ) : (
          <span className="abt-kpi__num">
            {value}
            {unit && <span className="abt-kpi__unit">{unit}</span>}
          </span>
        )}
      </div>
      {(deltaNode || caption) && (
        <div className="abt-kpi__meta">
          {deltaNode}
          {caption && <span className="abt-kpi__caption">{caption}</span>}
        </div>
      )}
      {href && (
        <a className="abt-kpi__link" href={href}>
          {linkLabel}
        </a>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ BudgetBar */

export function BudgetBar({ budget = 0, actual = 0, currency, label, warnAt = 1, critAt = 1.1, size = 'md', showValues }: any) {
  const b = Number(budget) || 0;
  const a = Number(actual) || 0;
  const max = Math.max(b, a) || 1;
  const ratio = b ? a / b : a ? Infinity : 0;
  const over = b > 0 && a > b;
  const tone = ratio >= critAt ? 'critical' : ratio > warnAt ? 'attention' : null;
  const planW = (b / max) * 100;
  const fillW = (Math.min(a, b || a) / max) * 100;
  const overW = over ? ((a - b) / max) * 100 : 0;
  const pct = b ? Math.round(ratio * 1000) / 10 : null;
  const show = showValues ?? size !== 'sm';
  const diff = a - b;
  const aria = `예산 ${formatNumber(b)} 대비 실제 ${formatNumber(a)}${currency ? ' ' + currency : ''}${pct != null ? `, ${pct}%` : ''}`;
  const track = (
    <div className="abt-budget__track" role="img" aria-label={aria}>
      {b > 0 && <span className="abt-budget__plan" style={{ width: planW + '%' }} />}
      {a > 0 && <span className="abt-budget__fill" style={{ width: fillW + '%' }} />}
      {over && <span className="abt-budget__over" style={{ left: `calc(${planW}% + 2px)`, width: `calc(${overW}% - 2px)` }} />}
    </div>
  );
  if (size === 'sm') {
    return (
      <div className={cx('abt-budget', 'abt-budget--sm', tone && `is-${tone}`)}>
        {track}
        <span className="abt-budget__pct">{pct != null ? `${pct}%` : '—'}</span>
      </div>
    );
  }
  return (
    <div className={cx('abt-budget', 'abt-budget--md', tone && `is-${tone}`)}>
      {(label || show) && (
        <div className="abt-budget__head">
          {label && <span className="abt-budget__label">{label}</span>}
          {show && (
            <span className="abt-budget__values">
              <Money amount={a} currency={currency} size="sm" />
              <span className="abt-muted">/</span>
              <Money amount={b} currency={currency} size="sm" kind="expected" />
            </span>
          )}
        </div>
      )}
      {track}
      <div className="abt-budget__foot">
        <span className="abt-budget__pct">{pct != null ? `예산의 ${pct}%` : '예산 없음'}</span>
        {over ? (
          <span className="abt-budget__diff">
            {formatNumber(diff)} {currency} 초과
          </span>
        ) : b > 0 ? (
          <span className="abt-budget__rest">
            잔여 {formatNumber(b - a)} {currency}
          </span>
        ) : null}
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ DataTable */

function alignOf(col: any) {
  if (col.align) return col.align;
  if (['money', 'number', 'percent'].includes(col.type)) return 'end';
  return 'start';
}

function renderCell(col: any, row: any) {
  const v = row[col.key];
  if (v == null || v === '') return <span className="abt-muted">—</span>;
  switch (col.type) {
    case 'code':
      return <EventCode code={v} href={row[col.hrefKey || 'href']} size="sm" />;
    case 'money': {
      const m = typeof v === 'object' ? v : { amount: v };
      return <Money currency={col.currency} kind={col.kind} lossTone={col.lossTone} {...m} size="sm" />;
    }
    case 'number':
      return (
        <span className="abt-num">
          {formatNumber(Number(v), col.digits ?? 0)}
          {col.suffix}
        </span>
      );
    case 'percent': {
      const n = Number(v);
      return (
        <span className={cx('abt-num', col.lossTone && n < 0 && 'abt-text-critical')}>
          {n < 0 ? '−' : ''}
          {Math.abs(n).toFixed(col.digits ?? 1)}%
        </span>
      );
    }
    case 'status': {
      const s = typeof v === 'object' ? v : { axis: col.axis, status: v };
      return <StatusBadge {...s} />;
    }
    case 'flags':
      return (
        <span className="abt-flags">
          {(Array.isArray(v) ? v : [v]).map((f: string) => (
            <StatusBadge key={f} axis="risk" status={f} />
          ))}
        </span>
      );
    case 'datetime': {
      const d = typeof v === 'object' ? v : { value: v };
      return <DateTime format={col.format || 'datetime'} zone={col.zone} {...d} />;
    }
    case 'budget':
      return <BudgetBar size="sm" currency={col.currency} warnAt={col.warnAt} critAt={col.critAt} {...v} />;
    case 'stack':
      return (
        <span className="abt-stack">
          <span>{v.primary}</span>
          {v.secondary && <span className="abt-muted">{v.secondary}</span>}
        </span>
      );
    case 'strong':
      return <span className="abt-strong">{v}</span>;
    case 'muted':
      return <span className="abt-muted">{v}</span>;
    default:
      return v;
  }
}

export function DataTable({ columns = [], rows = [], density = 'regular', caption, captionVisible, totals, selectable, stickyHeader = true, maxHeight, empty = '표시할 항목이 없습니다.', sort, onSort, onRowClick }: any) {
  const [sel, setSel] = useState(() => new Set(rows.filter((r: any) => r.selected).map((r: any) => r.id)));
  const toggle = (id: any) => {
    const next = new Set(sel);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    setSel(next);
  };
  const allOn = rows.length > 0 && rows.every((r: any) => sel.has(r.id));
  // A row with `href` opens it when clicked anywhere outside its own links and controls.
  const openRow = (e: any) => {
    const t = e.target;
    if (t && t.closest && t.closest('a,button,input,select,textarea,label')) return;
    const a = e.currentTarget.querySelector('a[data-row-link]') || e.currentTarget.querySelector('a[href]');
    if (a) a.click();
  };
  return (
    <div className={cx('abt-table-wrap', maxHeight && 'is-scroll')} style={maxHeight ? { maxHeight } : undefined}>
      <table className={cx('abt-table', `abt-table--${density}`, stickyHeader && 'is-sticky')}>
        {caption && <caption className={captionVisible ? 'abt-table__caption' : 'abt-sr'}>{caption}</caption>}
        <thead>
          <tr>
            {selectable && (
              <th className="abt-table__check" scope="col">
                <input type="checkbox" aria-label="전체 선택" checked={allOn} onChange={() => setSel(allOn ? new Set() : new Set(rows.map((r: any) => r.id)))} />
              </th>
            )}
            {columns.map((col: any) => {
              const active = sort && sort.key === col.key;
              return (
                <th
                  key={col.key}
                  scope="col"
                  className={cx(`is-${alignOf(col)}`, col.sortable && 'is-sortable')}
                  style={col.width ? { width: col.width } : undefined}
                  aria-sort={active ? (sort.dir === 'asc' ? 'ascending' : 'descending') : undefined}
                >
                  {col.sortable ? (
                    <button type="button" className="abt-sort" onClick={() => onSort && onSort(col.key)}>
                      {col.label}
                      <Icon name={active ? (sort.dir === 'asc' ? 'chevron-up' : 'chevron-down') : 'chevrons-up-down'} size={14} />
                    </button>
                  ) : (
                    col.label
                  )}
                </th>
              );
            })}
          </tr>
        </thead>
        <tbody>
          {rows.length ? (
            rows.map((row: any, i: number) => {
              const id = row.id ?? i;
              const isSel = selectable ? sel.has(id) : !!row.selected;
              return (
                <tr
                  key={id}
                  className={cx(isSel && 'is-selected', row.dim && 'is-dim', (onRowClick || row.href) && 'is-clickable')}
                  onClick={onRowClick ? () => onRowClick(row) : row.href ? openRow : undefined}
                >
                  {selectable && (
                    <td className="abt-table__check">
                      <input type="checkbox" aria-label={`${row.label ?? id} 선택`} checked={isSel} onChange={() => toggle(id)} onClick={(e: any) => e.stopPropagation()} />
                    </td>
                  )}
                  {columns.map((col: any, ci: number) => (
                    <td key={col.key} className={cx(`is-${alignOf(col)}`, col.wrap && 'is-wrap')}>
                      {ci === 0 && row.href && !onRowClick && <a data-row-link="" className="abt-row-link" href={row.href} tabIndex={-1} aria-hidden="true" />}
                      {renderCell(col, row)}
                    </td>
                  ))}
                </tr>
              );
            })
          ) : (
            <tr>
              <td colSpan={columns.length + (selectable ? 1 : 0)} className="abt-table__empty">
                {empty}
              </td>
            </tr>
          )}
        </tbody>
        {totals && (
          <tfoot>
            <tr>
              {selectable && <td />}
              {columns.map((col: any, idx: number) => (
                <td key={col.key} className={`is-${alignOf(col)}`}>
                  {totals[col.key] !== undefined ? renderCell(col, totals) : idx === 0 ? totals.label ?? '합계' : null}
                </td>
              ))}
            </tr>
          </tfoot>
        )}
      </table>
    </div>
  );
}

/* ------------------------------------------------------------------ ApprovalSteps */

const STEP_STATE: Record<string, string> = { done: '완료', current: '진행 중', pending: '대기', rejected: '반려', skipped: '생략' };

export function ApprovalSteps({ steps = [], orientation = 'horizontal' }: any) {
  return (
    <ol className={cx('abt-steps', `abt-steps--${orientation}`)}>
      {steps.map((s: any, i: number) => {
        const state = s.state || 'pending';
        return (
          <li key={i} className={cx('abt-step', `is-${state}`)} aria-current={state === 'current' ? 'step' : undefined}>
            <span className="abt-step__marker" aria-hidden="true" />
            <span className="abt-step__body">
              <span className="abt-step__label">
                {s.label}
                <span className="abt-sr"> ({STEP_STATE[state]})</span>
              </span>
              {(s.actor || s.at) && (
                <span className="abt-step__meta">
                  {s.actor && <span>{s.actor}</span>}
                  {s.at && <span>{s.at}</span>}
                </span>
              )}
              {s.note && <span className="abt-step__note">{s.note}</span>}
            </span>
          </li>
        );
      })}
    </ol>
  );
}

/* ------------------------------------------------------------------ AuditLog */

export function AuditLog({ entries = [], zone = 'KST' }: any) {
  return (
    <ol className="abt-audit">
      {entries.map((e: any, i: number) => (
        <li key={i} className="abt-audit__item">
          <DateTime value={e.at} zone={e.zone || zone} format="datetime" />
          <div className="abt-audit__body">
            <div className="abt-audit__who">
              <span className="abt-strong">{e.actor}</span>
              {e.role && <span className="abt-muted">{e.role}</span>}
              <span>{e.action}</span>
            </div>
            {e.field && (
              <div className="abt-audit__change">
                <span className="abt-muted">{e.field}</span>
                {e.before != null && <del className="abt-audit__before">{e.before}</del>}
                {e.before != null && <span aria-hidden="true">→</span>}
                <ins className="abt-audit__after">{e.after}</ins>
              </div>
            )}
            {e.reason && <div className="abt-audit__note">사유: {e.reason}</div>}
            {e.approver && <div className="abt-audit__note">승인: {e.approver}</div>}
          </div>
        </li>
      ))}
    </ol>
  );
}

/* ------------------------------------------------------------------ Alert */

export function Alert({ tone = 'attention', title, children, action, actions }: any) {
  return (
    <div className={cx('abt-alert', `abt-alert--${tone}`)} role={tone === 'critical' ? 'alert' : 'status'}>
      <div className="abt-alert__text">
        {title && <p className="abt-alert__title">{title}</p>}
        {children && <div className="abt-alert__body">{children}</div>}
      </div>
      {(action || actions) && (
        <div className="abt-alert__actions">
          {actions}
          {action && (
            <Button size="sm" href={action.href} onClick={action.onClick}>
              {action.label}
            </Button>
          )}
        </div>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ ScheduleGrid */

const BAR_PREFIX: Record<string, string> = { changed: '변경', conflict: '충돌' };
const BAR_STATE: Record<string, string> = { confirmed: '배정 확정', tentative: '가배정', changed: '변경 확인 필요', conflict: '일정 충돌', off: '배정 불가' };

function layoutRow(items: any[], detect: boolean) {
  const sorted = items.map((it, i) => ({ ...it, _i: i })).sort((a, b) => a.start - b.start || b.span - a.span);
  const laneEnds: number[] = [];
  for (const it of sorted) {
    let lane = laneEnds.findIndex((end) => end <= it.start);
    if (lane === -1) {
      lane = laneEnds.length;
      laneEnds.push(0);
    }
    laneEnds[lane] = it.start + it.span;
    it._lane = lane;
  }
  if (detect) {
    for (let i = 0; i < sorted.length; i++)
      for (let j = i + 1; j < sorted.length; j++) {
        const a = sorted[i];
        const b = sorted[j];
        if (a.start < b.start + b.span && b.start < a.start + a.span) {
          if (a.state !== 'off') a._conflict = true;
          if (b.state !== 'off') b._conflict = true;
        }
      }
  }
  return { items: sorted, lanes: Math.max(1, laneEnds.length) };
}

export function ScheduleGrid({ days = [], rows = [], cellWidth = 40, labelWidth = 184, rowLabel = '가이드', detectConflicts = true, caption }: any) {
  const n = days.length;
  const cols = `${labelWidth}px repeat(${n}, ${cellWidth}px)`;
  const LANE = 28;
  return (
    <div className="abt-sched" role="region" aria-label={caption || '배정 캘린더'}>
      <div className="abt-sched__grid" style={{ width: labelWidth + n * cellWidth }}>
        <div className="abt-sched__head" style={{ gridTemplateColumns: cols }}>
          <div className="abt-sched__corner">{rowLabel}</div>
          {days.map((d: any, i: number) => (
            <div key={i} className={cx('abt-sched__day', d.weekend && 'is-weekend', d.today && 'is-today')}>
              <b>{d.label}</b>
              <span>{d.dow}</span>
            </div>
          ))}
        </div>
        {rows.map((r: any) => {
          const { items, lanes } = layoutRow(r.items || [], detectConflicts);
          const h = lanes * LANE + 8;
          return (
            <div key={r.id ?? r.name} className="abt-sched__row" style={{ gridTemplateColumns: cols, minHeight: Math.max(h, 48) }}>
              <div className="abt-sched__label">
                <span className="abt-sched__name">{r.name}</span>
                {r.meta && <span className="abt-sched__meta">{r.meta}</span>}
              </div>
              <div className="abt-sched__lane" style={{ height: Math.max(h, 48) }}>
                {days.map((d: any, i: number) => (
                  <span key={i} className={cx('abt-sched__col', d.weekend && 'is-weekend', d.today && 'is-today')} style={{ left: i * cellWidth, width: cellWidth }} />
                ))}
                {items.map((it: any) => {
                  const state = it._conflict && it.state !== 'off' ? 'conflict' : it.state || 'confirmed';
                  const prefix = it.prefix ?? BAR_PREFIX[state];
                  const Tag: any = it.href ? 'a' : 'span';
                  const full = `${it.prefix || BAR_STATE[state] || ''} · ${it.label}${it.sub ? ' · ' + it.sub : ''}`;
                  return (
                    <Tag
                      key={it._i}
                      href={it.href}
                      className={cx('abt-sched__bar', `is-${state}`)}
                      style={{ left: it.start * cellWidth + 2, width: it.span * cellWidth - 4, top: 4 + it._lane * LANE }}
                      title={full}
                      aria-label={full}
                    >
                      {prefix && <b>{prefix}</b>}
                      <span>{it.label}</span>
                    </Tag>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ Tabs & Segmented */

export function Tabs({ items = [], value, onChange, ariaLabel, 'aria-label': ariaLabelAttr }: any) {
  const name = ariaLabel ?? ariaLabelAttr;
  const [cur, setCur] = useState(value ?? items[0]?.id);
  const v = value ?? cur;
  return (
    <div className="abt-tabs" role="tablist" aria-label={name}>
      {items.map((it: any) => {
        const active = it.id === v;
        const content = (
          <>
            {it.label}
            {it.count != null && <span className={cx('abt-count', it.tone && `abt-count--${it.tone}`)}>{it.count}</span>}
          </>
        );
        return it.href ? (
          <a key={it.id} role="tab" aria-selected={active} className={cx('abt-tabs__tab', active && 'is-active')} href={it.href}>
            {content}
          </a>
        ) : (
          <button
            key={it.id}
            type="button"
            role="tab"
            aria-selected={active}
            className={cx('abt-tabs__tab', active && 'is-active')}
            onClick={() => {
              setCur(it.id);
              onChange && onChange(it.id);
            }}
          >
            {content}
          </button>
        );
      })}
    </div>
  );
}

export function Segmented({ options = [], value, onChange, size = 'md', ariaLabel, 'aria-label': ariaLabelAttr }: any) {
  const name = ariaLabel ?? ariaLabelAttr;
  const opts = options.map((o: any) => (typeof o === 'string' ? { value: o, label: o } : o));
  const [cur, setCur] = useState(value ?? opts[0]?.value);
  const v = value ?? cur;
  return (
    <div className={cx('abt-seg', `abt-seg--${size}`)} role="group" aria-label={name}>
      {opts.map((o: any) => (
        <button
          key={o.value}
          type="button"
          aria-pressed={o.value === v}
          className={cx('abt-seg__opt', o.value === v && 'is-active')}
          onClick={() => {
            setCur(o.value);
            onChange && onChange(o.value);
          }}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}

/* ------------------------------------------------------------------ Fields */

function useFieldId(id?: string) {
  const auto = useId ? useId() : 'f' + Math.random().toString(36).slice(2);
  return id || 'abt' + auto.replace(/:/g, '');
}

export function TextField({ label, ariaLabel, 'aria-label': ariaLabelAttr, tag, value, defaultValue, placeholder, help, error, prefix, suffix, required, readOnly, locked, type = 'text', size = 'md', align, multiline, rows = 3, onChange, id, name, inputMode }: any) {
  const fid = useFieldId(id);
  const controlled = value !== undefined && typeof onChange === 'function';
  const ro = readOnly || locked;
  const helpText = error || (locked ? help || '마감된 자료입니다. 재개방 승인 후 수정할 수 있습니다.' : help);
  const common = {
    id: fid,
    name,
    className: cx('abt-input', align === 'end' && 'is-end'),
    placeholder,
    readOnly: ro,
    required,
    'aria-label': label ? undefined : ariaLabel ?? ariaLabelAttr,
    'aria-invalid': error ? true : undefined,
    'aria-describedby': helpText ? fid + '-help' : undefined,
    onChange,
    value: controlled ? value : undefined,
    defaultValue: controlled ? undefined : value ?? defaultValue,
  };
  return (
    <div className={cx('abt-field', `abt-field--${size}`, error && 'is-invalid', locked && 'is-locked')}>
      {label && (
        <label className="abt-field__label" htmlFor={fid}>
          {label}
          {required && <span className="abt-field__req">필수</span>}
          {tag && <span className="abt-field__tag">{tag}</span>}
        </label>
      )}
      <div className={cx('abt-field__control', multiline && 'is-multiline')}>
        {prefix && <span className="abt-field__affix">{prefix}</span>}
        {multiline ? <textarea rows={rows} {...common} /> : <input type={type} inputMode={inputMode} {...common} />}
        {suffix && <span className="abt-field__affix">{suffix}</span>}
        {locked && <span className="abt-field__lock">마감</span>}
      </div>
      {helpText && (
        <p id={fid + '-help'} className={cx('abt-field__help', error && 'is-error')}>
          {helpText}
        </p>
      )}
    </div>
  );
}

export function Select({ label, options = [], value, defaultValue, onChange, help, error, size = 'md', inline, id, disabled, required }: any) {
  const fid = useFieldId(id);
  const opts = options.map((o: any) => (typeof o === 'string' ? { value: o, label: o } : o));
  const controlled = value !== undefined && typeof onChange === 'function';
  const sel = (
    <select
      id={fid}
      disabled={disabled}
      required={required}
      value={controlled ? value : undefined}
      defaultValue={controlled ? undefined : value ?? defaultValue}
      onChange={onChange}
      aria-invalid={error ? true : undefined}
      aria-describedby={error || help ? fid + '-help' : undefined}
    >
      {opts.map((o: any) => (
        <option key={o.value} value={o.value}>
          {o.label}
        </option>
      ))}
    </select>
  );
  if (inline) {
    return (
      <div className={cx('abt-select', 'abt-select--inline', `abt-select--${size}`)}>
        <div className="abt-select__control">
          <label className="abt-select__inline-label" htmlFor={fid}>
            {label}
          </label>
          {sel}
          <Icon name="chevron-down" size={16} className="abt-select__chev" />
        </div>
      </div>
    );
  }
  return (
    <div className={cx('abt-field', 'abt-select', `abt-field--${size}`, `abt-select--${size}`, error && 'is-invalid')}>
      {label && (
        <label className="abt-field__label" htmlFor={fid}>
          {label}
          {required && <span className="abt-field__req">필수</span>}
        </label>
      )}
      <div className="abt-select__control">
        {sel}
        <Icon name="chevron-down" size={16} className="abt-select__chev" />
      </div>
      {(error || help) && (
        <p id={fid + '-help'} className={cx('abt-field__help', error && 'is-error')}>
          {error || help}
        </p>
      )}
    </div>
  );
}

export function MoneyField({ label, tag, amount, currency = 'MNT', currencies = ['MNT', 'KRW', 'USD'], rate, help, error, size = 'md', required, id, onAmountChange, onCurrencyChange }: any) {
  const fid = useFieldId(id);
  const [cur, setCur] = useState(currency);
  const [amt, setAmt] = useState(amount == null ? '' : formatNumber(Number(amount), CURRENCIES[currency]?.digits ?? 0));
  const numeric = Number(String(amt).replace(/[^0-9.\-]/g, ''));
  const conv = rate && amt !== '' && !Number.isNaN(numeric) ? numeric * rate.value : null;
  return (
    <div className={cx('abt-field', 'abt-money-field', `abt-field--${size}`, error && 'is-invalid')}>
      {label && (
        <label className="abt-field__label" htmlFor={fid}>
          {label}
          {required && <span className="abt-field__req">필수</span>}
          {tag && <span className="abt-field__tag">{tag}</span>}
        </label>
      )}
      <div className="abt-field__control">
        <input
          id={fid}
          className="abt-input is-end"
          inputMode="decimal"
          value={amt}
          aria-invalid={error ? true : undefined}
          aria-describedby={fid + '-help'}
          onChange={(e: any) => {
            setAmt(e.target.value);
            onAmountChange && onAmountChange(e.target.value);
          }}
        />
        <span className="abt-money-field__cur">
          <select
            aria-label="통화"
            value={cur}
            onChange={(e: any) => {
              setCur(e.target.value);
              onCurrencyChange && onCurrencyChange(e.target.value);
            }}
          >
            {currencies.map((c: string) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
          <Icon name="chevron-down" size={14} className="abt-select__chev" />
        </span>
      </div>
      <p id={fid + '-help'} className={cx('abt-field__help', error && 'is-error')}>
        {error ||
          (conv != null && cur !== rate.base ? (
            <>
              ≈ {formatMoney(conv, rate.base)} {rate.base} · 환율 {rate.value}
              {rate.date ? ` (${rate.date} 적용)` : ''}
            </>
          ) : (
            help || '원래 통화 그대로 입력하세요. 환산액은 적용 환율로 따로 저장됩니다.'
          ))}
      </p>
    </div>
  );
}

export function Checkbox({ label, description, checked, defaultChecked, onChange, disabled, id }: any) {
  const fid = useFieldId(id);
  const controlled = checked !== undefined && typeof onChange === 'function';
  return (
    <label className={cx('abt-check', disabled && 'is-disabled')} htmlFor={fid}>
      <input
        id={fid}
        type="checkbox"
        disabled={disabled}
        checked={controlled ? checked : undefined}
        defaultChecked={controlled ? undefined : checked ?? defaultChecked}
        onChange={onChange}
      />
      <span className="abt-check__text">
        <span>{label}</span>
        {description && <span className="abt-check__desc">{description}</span>}
      </span>
    </label>
  );
}

/* ------------------------------------------------------------------ Attachment */

const ATTACH_KIND: Record<string, string> = { receipt: '영수증', photo: '사진', doc: '문서', confirmation: '예약 확인서', proof: '송금 증빙' };

export function Attachment({ name, kind = 'receipt', meta, missing, href }: any) {
  const kindLabel = ATTACH_KIND[kind] || kind;
  if (missing) {
    return (
      <span className="abt-attach is-missing">
        <span className="abt-attach__kind">{kindLabel}</span>
        <span>증빙 누락</span>
      </span>
    );
  }
  const Tag: any = href ? 'a' : 'span';
  return (
    <Tag className="abt-attach" href={href}>
      <span className="abt-attach__kind">{kindLabel}</span>
      <span className="abt-attach__name">{name}</span>
      {meta && <span className="abt-attach__meta">{meta}</span>}
    </Tag>
  );
}

/* ------------------------------------------------------------------ SideNav */

export const NAV_SECTIONS = [
  {
    title: '현황',
    items: [
      { id: 'dashboard', label: '대시보드', icon: 'layout-dashboard' },
      { id: 'alerts', label: '알림', icon: 'bell' },
      { id: 'reports', label: '리포트', icon: 'file-spreadsheet' },
    ],
  },
  {
    title: '운영',
    items: [
      { id: 'events', label: '행사', icon: 'calendar-days' },
      { id: 'schedule', label: '배정 캘린더', icon: 'calendar-range' },
      { id: 'field', label: '현장 보고', icon: 'clipboard-check' },
      { id: 'claims', label: '클레임', icon: 'message-square-warning' },
    ],
  },
  {
    title: '회계',
    items: [
      { id: 'receipts', label: '입금', icon: 'wallet' },
      { id: 'costs', label: '지상비·비용', icon: 'receipt' },
      { id: 'remit', label: '송금', icon: 'send' },
      { id: 'balance', label: '과입·차감', icon: 'arrow-left-right' },
      { id: 'settlement', label: '정산·마감', icon: 'scale' },
    ],
  },
  {
    title: '기준정보',
    items: [
      { id: 'agencies', label: '여행사', icon: 'building-2' },
      { id: 'products', label: '상품', icon: 'package' },
      { id: 'partners', label: '협력업체·요금표', icon: 'hotel' },
      { id: 'resources', label: '가이드·차량', icon: 'users' },
      { id: 'manuals', label: '매뉴얼', icon: 'book-open' },
    ],
  },
  {
    title: '관리',
    items: [
      { id: 'users', label: '사용자·권한', icon: 'user-cog' },
      { id: 'audit', label: '감사 로그', icon: 'history' },
    ],
  },
];

export const THEME_OPTIONS = [
  { value: 'dark', label: '다크' },
  { value: 'light', label: '라이트' },
];

export function SideNav({ active, sections = NAV_SECTIONS, links = {}, counts = {}, product = 'ABT Ops', org, user, logout, theme, onThemeChange }: any) {
  return (
    <nav className="abt-nav" aria-label="주 메뉴">
      <div className="abt-nav__brand">
        <span className="abt-nav__product">{product}</span>
        {org && <span className="abt-nav__org">{org}</span>}
      </div>
      <div className="abt-nav__sections">
        {sections.map((sec: any) => (
          <div key={sec.title} className="abt-nav__section">
            <p className="abt-nav__title">{sec.title}</p>
            <ul>
              {sec.items.map((it: any) => {
                const c = counts[it.id];
                const n = c == null ? null : typeof c === 'object' ? c.n : c;
                const tone = c && typeof c === 'object' ? c.tone : null;
                const on = active === it.id;
                return (
                  <li key={it.id}>
                    <a className={cx('abt-nav__item', on && 'is-active')} href={links[it.id] || it.href || '#'} aria-current={on ? 'page' : undefined}>
                      <Icon name={it.icon} size={18} />
                      <span className="abt-nav__label">{it.label}</span>
                      {n != null && <span className={cx('abt-count', tone && `abt-count--${tone}`)}>{n}</span>}
                    </a>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </div>
      {onThemeChange && (
        <div className="abt-nav__theme">
          <span className="abt-nav__theme-label">화면</span>
          <Segmented size="sm" options={THEME_OPTIONS} value={theme || 'dark'} onChange={onThemeChange} ariaLabel="화면 테마" />
        </div>
      )}
      {user && (
        <div className="abt-nav__user">
          <span className="abt-nav__avatar" aria-hidden="true">
            {String(user.name || '').slice(0, 1)}
          </span>
          <span className="abt-nav__user-text">
            <span className="abt-nav__user-name">{user.name}</span>
            <span className="abt-nav__user-role">{user.role}</span>
          </span>
          {logout && (
            <a className="abt-nav__logout" href={logout}>
              로그아웃
            </a>
          )}
        </div>
      )}
    </nav>
  );
}

/* ------------------------------------------------------------------ MobileTabBar */

export const TAB_ITEMS = [
  { id: 'today', label: '오늘', icon: 'house' },
  { id: 'schedule', label: '내 일정', icon: 'calendar-days' },
  { id: 'add', label: '현장 등록', icon: 'plus', primary: true },
  { id: 'settle', label: '내 정산', icon: 'wallet' },
  { id: 'notice', label: '알림', icon: 'bell' },
];

export function MobileTabBar({ items = TAB_ITEMS, active, links = {}, badges = {} }: any) {
  return (
    <nav className="abt-tabbar" aria-label="하단 메뉴">
      {items.map((it: any) => {
        const on = active === it.id;
        const badge = badges[it.id];
        return (
          <a key={it.id} href={links[it.id] || it.href || '#'} className={cx('abt-tabbar__item', on && 'is-active', it.primary && 'is-primary')} aria-current={on ? 'page' : undefined}>
            <span className="abt-tabbar__icon">
              <Icon name={it.icon} size={22} />
              {badge != null && <span className="abt-tabbar__badge">{badge}</span>}
            </span>
            <span className="abt-tabbar__label">
              {it.label}
              {badge != null && <span className="abt-sr"> {badge}건</span>}
            </span>
          </a>
        );
      })}
    </nav>
  );
}

/* ------------------------------------------------------------------ export */

const api = {
  Icon,
  Button,
  StatusBadge,
  Money,
  EventCode,
  DateTime,
  KpiTile,
  DataTable,
  BudgetBar,
  ApprovalSteps,
  AuditLog,
  Alert,
  ScheduleGrid,
  Tabs,
  Segmented,
  TextField,
  Select,
  MoneyField,
  Checkbox,
  Attachment,
  SideNav,
  MobileTabBar,
  STATUS,
  NAV_SECTIONS,
  THEME_OPTIONS,
  TAB_ITEMS,
  statusLabel,
  formatMoney,
  formatNumber,
  formatCompact,
};
const W: any = window as any;
W.Abt = Object.assign(W.Abt || {}, api);
