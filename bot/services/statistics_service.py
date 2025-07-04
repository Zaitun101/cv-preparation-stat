from analytics.analytics import Analytics
from databases.mongo import Mongo


class StatisticsService:
    def __init__(self):
        self.mongo = Mongo()
        self.analytics = Analytics()

    def get_general_statistics(self, events: list) -> list[str]:
        stats = self.analytics.get_general_analytics(events)
        report_lines = [
            '📊 Общая статистика:',
            f'   🤖 всего запусков бота: {stats["total_runs"]}',
            f'   🤖 bot_result событий: {stats["bot_results"]}',
            f'   🤖 bot_attempt событий: {stats["bot_attempts"]}',
            f'\n✅ {stats["success_count"]} — {stats["success_percent"]:.1f}% | '
            f'❌ {stats["fail_count"]} — {stats["fail_percent"]:.1f}%'
            f'\n\nДетализация фейлов по статусам:',
        ]

        if stats['fail_details']:
            for fail_type, count in sorted(
                stats['fail_details'].items(), key=lambda x: x[1], reverse=True
            ):
                report_lines.append(f'     - {fail_type}: {count}')
        else:
            report_lines.append('     Нет фейлов')

        return report_lines

    def get_grouped_statistics(
        self, events: list, group_field: str, title: str, item_title: str
    ) -> list[str]:
        report_lines = []
        stats = self.analytics.get_analytics(events, group_field)
        risky_items = []

        report_lines.append(f'\n📊 {title}:')
        if stats.empty:
            report_lines.append('Нет данных для отображения')
            return report_lines

        for _, row in stats.iterrows():
            value = row[group_field]
            if group_field == 'game_id' and isinstance(value, float):
                value = int(value)
            total = int(row['total'])
            success = int(row['success'])
            fail = int(row['fail'])
            success_percent = row['success_percent']
            fail_percent = row['fail_percent']

            report_lines.append(f'\n📌 {item_title} {value}:')
            report_lines.append(
                f'✅ {success} — {success_percent:.1f}% | ❌ {fail} — {fail_percent:.1f}%'
            )

            if fail > 0:
                report_lines.append('Подробности фейлов:')
                fail_details = self.analytics.count_fail_statuses(
                    events, group_field, value
                )
                for fail_type, count in fail_details.items():
                    report_lines.append(f'    - {fail_type}: {count}')

            if fail_percent > 30 and total > 5:
                risky_items.append((value, fail_percent, total))

        if risky_items:
            report_lines.append(f'\n🚨 {item_title}(ы) с процентом фейлов выше 30%:')
            for value, percent, total in risky_items:
                report_lines.append(
                    f'     • {item_title} {value}: {percent:.1f}% при {total} запусках'
                )

        return report_lines

    def get_adopt_statistics(self, events: list) -> list[str]:
        adopt_df = self.analytics.filter_adopt_fail_events(events)

        if adopt_df.empty:
            return []

        report_lines = []
        for i, (_, row) in enumerate(adopt_df.iterrows(), 1):
            report_lines.append(
                f'{i}\n'
                f'bot_id: {row.get("bot_id", "-")}\n'
                f'status: {row.get("status", "-")}\n'
                f'server_address: {row.get("server_address", "-")}\n'
                f'timestamp: {row.get("timestamp", "-")}\n'
                f'updated_at: {row.get("updated_at", "-")}\n'
            )

        return report_lines

    def get_game_statistics(self, events: list) -> list[str]:
        return self.get_grouped_statistics(
            events,
            group_field='game_id',
            title='Статистика по играм',
            item_title='Игра',
        )

    def get_server_statistics(self, events: list) -> list[str]:
        return self.get_grouped_statistics(
            events,
            group_field='server_address',
            title='Статистика по серверам',
            item_title='Сервер',
        )

    def get_alert_general_statistics(
        self, events: list
    ) -> list[int, int, float, int, float]:
        stats = self.analytics.get_general_analytics(events)
        return [
            stats['bot_results'],
            stats['success_count'],
            round(stats['success_percent'], 1),
            stats['fail_count'],
            round(stats['fail_percent'], 1),
        ]

    def start(self):
        hours = int(input('За сколько часов смотреть статистику: '))
        events = self.mongo.get_events(hours)

        for line in self.get_general_statistics(events):
            print(line)

        for line in self.get_game_statistics(events):
            print(line)

        for line in self.get_server_statistics(events):
            print(line)

        for line in self.get_adopt_statistics(events):
            print(line)


if __name__ == '__main__':
    StatisticsService().start()
