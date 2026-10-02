import type * as React from 'react';

export type Currency = 'KRW' | 'USD' | 'MNT';
export type Zone = 'KST' | 'ULAT';
export type Tone = 'neutral' | 'progress' | 'positive' | 'attention' | 'critical';
export type StatusForm = 'solid' | 'dashed' | 'strong';
export type StatusAxis = 'event' | 'cost' | 'remit' | 'payment' | 'settle' | 'assign' | 'claim' | 'report' | 'risk';

export interface IconProps { name: 'layout-dashboard' | 'bell' | 'file-spreadsheet' | 'calendar-days' | 'calendar-range' | 'clipboard-check' | 'message-square-warning' | 'wallet' | 'receipt' | 'send' | 'arrow-left-right' | 'scale' | 'building-2' | 'package' | 'hotel' | 'users' | 'book-open' | 'user-cog' | 'history' | 'log-out' | 'settings' | 'house' | 'plus' | 'chevron-down' | 'chevron-up' | 'chevrons-up-down' | 'chevron-left' | 'chevron-right' | 'x' | 'menu' | 'check'; size?: number; strokeWidth?: number; title?: string; className?: string }
export declare function Icon(props: IconProps): React.ReactElement | null;

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> { variant?: 'primary' | 'secondary' | 'ghost' | 'danger'; size?: 'sm' | 'md' | 'lg'; href?: string; block?: boolean }
export declare function Button(props: ButtonProps): React.ReactElement;

export interface StatusBadgeProps { axis?: StatusAxis; status?: string; tone?: Tone; form?: StatusForm; size?: 'sm' | 'md'; title?: string; children?: React.ReactNode }
export declare function StatusBadge(props: StatusBadgeProps): React.ReactElement;

export interface MoneyProps { amount: number; currency?: Currency; kind?: 'actual' | 'expected'; converted?: { amount: number; currency: Currency }; rate?: { value: number; date?: string }; size?: 'sm' | 'md' | 'lg' | 'kpi'; sign?: 'auto' | 'always'; compact?: boolean; tag?: boolean; lossTone?: boolean; align?: 'end' | 'start' }
export declare function Money(props: MoneyProps): React.ReactElement;

export interface EventCodeProps { code: string; href?: string; size?: 'sm' | 'md'; title?: string }
export declare function EventCode(props: EventCodeProps): React.ReactElement;

export interface DateTimeProps { value: string; zone?: Zone; format?: 'datetime' | 'date' | 'short' | 'time'; other?: boolean | Zone; showZone?: boolean }
export declare function DateTime(props: DateTimeProps): React.ReactElement;

export interface KpiTileProps { label: string; value?: React.ReactNode; unit?: string; money?: MoneyProps; delta?: { value: number; unit?: string; period?: string; good: 'up' | 'down'; digits?: number }; state?: 'attention' | 'critical'; stateLabel?: string; caption?: string; href?: string; linkLabel?: string }
export declare function KpiTile(props: KpiTileProps): React.ReactElement;

export interface BudgetBarProps { budget: number; actual: number; currency?: Currency; label?: string; warnAt?: number; critAt?: number; size?: 'sm' | 'md'; showValues?: boolean }
export declare function BudgetBar(props: BudgetBarProps): React.ReactElement;

export interface DataTableColumn { key: string; label: string; type?: 'text' | 'code' | 'money' | 'number' | 'percent' | 'status' | 'flags' | 'datetime' | 'budget' | 'stack' | 'strong' | 'muted'; align?: 'start' | 'end' | 'center'; width?: string; wrap?: boolean; sortable?: boolean; currency?: Currency; kind?: 'actual' | 'expected'; lossTone?: boolean; axis?: StatusAxis; zone?: Zone; format?: DateTimeProps['format']; suffix?: string; digits?: number; hrefKey?: string; warnAt?: number; critAt?: number }
export interface DataTableProps { columns: DataTableColumn[]; rows: Array<Record<string, any> & { id?: string | number; href?: string; selected?: boolean; dim?: boolean }>; density?: 'regular' | 'compact'; caption?: string; captionVisible?: boolean; totals?: Record<string, any> & { label?: string }; selectable?: boolean; stickyHeader?: boolean; maxHeight?: number | string; empty?: string; sort?: { key: string; dir: 'asc' | 'desc' }; onSort?: (key: string) => void; onRowClick?: (row: any) => void }
export declare function DataTable(props: DataTableProps): React.ReactElement;

export interface ApprovalStep { label: string; state?: 'done' | 'current' | 'pending' | 'rejected' | 'skipped'; actor?: string; at?: string; note?: string }
export interface ApprovalStepsProps { steps: ApprovalStep[]; orientation?: 'horizontal' | 'vertical' }
export declare function ApprovalSteps(props: ApprovalStepsProps): React.ReactElement;

export interface AuditEntry { at: string; zone?: Zone; actor: string; role?: string; action: string; field?: string; before?: string; after?: string; reason?: string; approver?: string }
export interface AuditLogProps { entries: AuditEntry[]; zone?: Zone }
export declare function AuditLog(props: AuditLogProps): React.ReactElement;

export interface AlertProps { tone?: 'progress' | 'positive' | 'attention' | 'critical'; title?: string; children?: React.ReactNode; action?: { label: string; href?: string; onClick?: () => void }; actions?: React.ReactNode }
export declare function Alert(props: AlertProps): React.ReactElement;

export interface ScheduleDay { label: string; dow: string; weekend?: boolean; today?: boolean }
export interface ScheduleItem { start: number; span: number; label: string; sub?: string; prefix?: string; state?: 'confirmed' | 'tentative' | 'changed' | 'conflict' | 'off'; href?: string }
export interface ScheduleGridProps { days: ScheduleDay[]; rows: Array<{ id?: string; name: string; meta?: string; items: ScheduleItem[] }>; cellWidth?: number; labelWidth?: number; rowLabel?: string; detectConflicts?: boolean; caption?: string }
export declare function ScheduleGrid(props: ScheduleGridProps): React.ReactElement;

export interface TabsProps { items: Array<{ id: string; label: string; count?: number; tone?: Tone; href?: string }>; value?: string; onChange?: (id: string) => void; ariaLabel?: string; 'aria-label'?: string }
export declare function Tabs(props: TabsProps): React.ReactElement;

export interface SegmentedProps { options: Array<string | { value: string; label: string }>; value?: string; onChange?: (value: string) => void; size?: 'sm' | 'md'; ariaLabel?: string; 'aria-label'?: string }
export declare function Segmented(props: SegmentedProps): React.ReactElement;

export interface TextFieldProps { label?: string; ariaLabel?: string; 'aria-label'?: string; tag?: string; value?: string; defaultValue?: string; placeholder?: string; help?: string; error?: string; prefix?: string; suffix?: string; required?: boolean; readOnly?: boolean; locked?: boolean; type?: string; size?: 'sm' | 'md' | 'lg'; align?: 'start' | 'end'; multiline?: boolean; rows?: number; onChange?: React.ChangeEventHandler<HTMLInputElement | HTMLTextAreaElement>; id?: string; name?: string; inputMode?: string }
export declare function TextField(props: TextFieldProps): React.ReactElement;

export interface SelectProps { label?: string; options: Array<string | { value: string; label: string }>; value?: string; defaultValue?: string; onChange?: React.ChangeEventHandler<HTMLSelectElement>; help?: string; error?: string; size?: 'sm' | 'md' | 'lg'; inline?: boolean; id?: string; disabled?: boolean; required?: boolean }
export declare function Select(props: SelectProps): React.ReactElement;

export interface MoneyFieldProps { label?: string; tag?: string; amount?: number; currency?: Currency; currencies?: Currency[]; rate?: { value: number; base: Currency; date?: string }; help?: string; error?: string; size?: 'sm' | 'md' | 'lg'; required?: boolean; id?: string; onAmountChange?: (raw: string) => void; onCurrencyChange?: (c: Currency) => void }
export declare function MoneyField(props: MoneyFieldProps): React.ReactElement;

export interface CheckboxProps { label: string; description?: string; checked?: boolean; defaultChecked?: boolean; onChange?: React.ChangeEventHandler<HTMLInputElement>; disabled?: boolean; id?: string }
export declare function Checkbox(props: CheckboxProps): React.ReactElement;

export interface AttachmentProps { name?: string; kind?: 'receipt' | 'photo' | 'doc' | 'confirmation' | 'proof'; meta?: string; missing?: boolean; href?: string }
export declare function Attachment(props: AttachmentProps): React.ReactElement;

export interface NavItem { id: string; label: string; icon: IconProps['name']; href?: string }
export interface SideNavProps { /** Shows a 다크/라이트 switch above the user row when given. */ theme?: 'dark' | 'light'; onThemeChange?: (theme: 'dark' | 'light') => void; logout?: string; active?: string; sections?: Array<{ title: string; items: NavItem[] }>; links?: Record<string, string>; counts?: Record<string, number | { n: number; tone?: Tone }>; product?: string; org?: string; user?: { name: string; role: string } }
export declare function SideNav(props: SideNavProps): React.ReactElement;

export interface MobileTabBarProps { items?: Array<{ id: string; label: string; icon: IconProps['name']; primary?: boolean; href?: string }>; active?: string; links?: Record<string, string>; badges?: Record<string, number> }
export declare function MobileTabBar(props: MobileTabBarProps): React.ReactElement;

export declare const STATUS: Record<StatusAxis, Record<string, { label: string; tone: Tone; form: StatusForm }>>;
export declare function statusLabel(axis: StatusAxis, status: string): string;
export declare function formatMoney(amount: number, currency?: Currency, opts?: { sign?: 'always'; compact?: boolean }): string;
export declare function formatNumber(n: number, digits?: number): string;
export declare function formatCompact(n: number): string;

declare global {
  interface Window {
    Abt: {
      Icon: typeof Icon; Button: typeof Button; StatusBadge: typeof StatusBadge; Money: typeof Money; EventCode: typeof EventCode; DateTime: typeof DateTime;
      KpiTile: typeof KpiTile; DataTable: typeof DataTable; BudgetBar: typeof BudgetBar; ApprovalSteps: typeof ApprovalSteps; AuditLog: typeof AuditLog; Alert: typeof Alert;
      ScheduleGrid: typeof ScheduleGrid; Tabs: typeof Tabs; Segmented: typeof Segmented; TextField: typeof TextField; Select: typeof Select; MoneyField: typeof MoneyField;
      Checkbox: typeof Checkbox; Attachment: typeof Attachment; SideNav: typeof SideNav; MobileTabBar: typeof MobileTabBar;
      STATUS: typeof STATUS; statusLabel: typeof statusLabel; formatMoney: typeof formatMoney; formatNumber: typeof formatNumber; formatCompact: typeof formatCompact;
    };
  }
}
