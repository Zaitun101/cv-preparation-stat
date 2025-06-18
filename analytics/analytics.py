import pandas as pd


class Analytics:
    def get_general_analytics(self, events: list) -> dict:
        result_events = [e for e in events if e.get('event_type') == 'bot_result']
        attempt_events = [e for e in events if e.get('event_type') == 'bot_attempt']

        total_runs = len(result_events) + len(attempt_events)
        bot_results = len(result_events)
        bot_attempts = len(attempt_events)

        success_count = sum(1 for e in result_events if e.get('status') == 'SUCCESS')
        fail_count = bot_results - success_count
        success_percent = (success_count / bot_results * 100) if bot_results else 0
        fail_percent = (fail_count / bot_results * 100) if bot_results else 0

        status_events = [e for e in result_events if 'status' in e]
        if status_events:
            fail_details = (
                pd.DataFrame(status_events)['status']
                .value_counts()
                .drop('SUCCESS', errors='ignore')
                .to_dict()
            )
        else:
            fail_details = {}

        return {
            'total_runs': total_runs,
            'bot_results': bot_results,
            'bot_attempts': bot_attempts,
            'success_count': success_count,
            'fail_count': fail_count,
            'success_percent': success_percent,
            'fail_percent': fail_percent,
            'fail_details': fail_details,
        }

    def get_analytics(self, events: list, param: str) -> pd.DataFrame:
        filtered_events = [e for e in events if e.get('event_type') == 'bot_result']

        if not filtered_events:
            return pd.DataFrame(
                columns=[
                    param,
                    'total',
                    'success',
                    'fail',
                    'success_percent',
                    'fail_percent',
                ]
            )

        df = pd.DataFrame(filtered_events)

        total_counts = df.groupby(param).size().rename('total')
        success_counts = (
            df[df['status'] == 'SUCCESS'].groupby(param).size().rename('success')
        )

        stats = pd.concat([total_counts, success_counts], axis=1).fillna(0)
        stats['fail'] = stats['total'] - stats['success']
        stats['success_percent'] = (stats['success'] / stats['total'] * 100).round(1)
        stats['fail_percent'] = (stats['fail'] / stats['total'] * 100).round(1)

        stats = stats.reset_index()

        return stats.sort_values(by=['total'], ascending=False)

    def count_fail_statuses(self, events: list, group_field: str, group_value) -> dict:
        df = pd.DataFrame(events)
        mask = (df[group_field] == group_value) & (df['status'] != 'SUCCESS')
        return df[mask]['status'].value_counts().to_dict()

    def filter_adopt_fail_events(self, events: list) -> pd.DataFrame:
        """Возвращает DataFrame с событиями для Adopt Me по нужным статусам"""
        df = pd.DataFrame(events)
        if df.empty:
            return pd.DataFrame()

        adopt_df = df[
            (df['game_id'] == 920587237)
            & (df['status'].isin(['EDUCATION_FAIL', 'OUTER_STAGE_FAIL']))
        ].copy()

        def format_datetime(value):
            if pd.isna(value):
                return ''
            try:
                formatted = value.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00:00'
                return formatted
            except Exception:
                return ''

        for col in ['timestamp', 'updated_at']:
            if col in adopt_df.columns:
                adopt_df[col] = adopt_df[col].apply(format_datetime)

        return adopt_df.sort_values(by='timestamp', ascending=False)
