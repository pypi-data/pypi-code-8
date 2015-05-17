# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('description', models.CharField(max_length=128)),
                ('numgotten', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'achievements',
            },
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=64)),
            ],
            options={
                'db_table': 'awards',
            },
        ),
        migrations.CreateModel(
            name='Gametype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=16)),
                ('description', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'gametypes',
            },
        ),
        migrations.CreateModel(
            name='LoginPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('login', models.CharField(unique=True, max_length=64)),
                ('ready', models.BooleanField(default=False)),
                ('valid', models.BooleanField(default=False)),
                ('profile_url', models.CharField(blank=True, max_length=255)),
                ('profile_url_rml', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'db_table': 'login_players',
            },
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('mapname', models.CharField(unique=True, max_length=64)),
            ],
            options={
                'db_table': 'mapnames',
            },
        ),
        migrations.CreateModel(
            name='MatchAward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('count', models.IntegerField(default=0)),
                ('award', models.ForeignKey(related_name='+', to='warmama.Award')),
            ],
            options={
                'db_table': 'match_awards',
            },
        ),
        migrations.CreateModel(
            name='MatchFrag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('time', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'frag_log',
            },
        ),
        migrations.CreateModel(
            name='MatchPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(blank=True, max_length=64)),
                ('score', models.IntegerField(default=0)),
                ('frags', models.IntegerField(default=0)),
                ('deaths', models.IntegerField(default=0)),
                ('teamkills', models.IntegerField(default=0)),
                ('suicides', models.IntegerField(default=0)),
                ('numrounds', models.IntegerField(default=0)),
                ('ga_taken', models.IntegerField(default=0)),
                ('ya_taken', models.IntegerField(default=0)),
                ('ra_taken', models.IntegerField(default=0)),
                ('mh_taken', models.IntegerField(default=0)),
                ('uh_taken', models.IntegerField(default=0)),
                ('quads_taken', models.IntegerField(default=0)),
                ('shells_taken', models.IntegerField(default=0)),
                ('bombs_planted', models.IntegerField(default=0)),
                ('bombs_defused', models.IntegerField(default=0)),
                ('flags_capped', models.IntegerField(default=0)),
                ('matchtime', models.IntegerField(default=0)),
                ('oldrating', models.DecimalField(max_digits=8, default=0, decimal_places=2)),
                ('newrating', models.DecimalField(max_digits=8, default=0, decimal_places=2)),
            ],
            options={
                'db_table': 'match_players',
            },
        ),
        migrations.CreateModel(
            name='MatchResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('uuid', models.CharField(unique=True, default=uuid.uuid4, max_length=36)),
                ('instagib', models.BooleanField(default=False)),
                ('teamgame', models.BooleanField(default=False)),
                ('timelimit', models.IntegerField(default=0)),
                ('scorelimit', models.IntegerField(default=0)),
                ('gamedir', models.CharField(blank=True, max_length=64)),
                ('matchtime', models.IntegerField(default=0)),
                ('utctime', models.DateTimeField()),
                ('demo_filename', models.CharField(blank=True, max_length=128)),
                ('gametype', models.ForeignKey(related_name='matches', to='warmama.Gametype')),
                ('map', models.ForeignKey(related_name='matches', to='warmama.Map')),
            ],
            options={
                'db_table': 'match_results',
            },
        ),
        migrations.CreateModel(
            name='MatchTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('score', models.IntegerField(default=0)),
                ('matchresult', models.ForeignKey(related_name='teams', to='warmama.MatchResult')),
            ],
            options={
                'db_table': 'match_teams',
            },
        ),
        migrations.CreateModel(
            name='MatchWeapon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('shots_strong', models.IntegerField(default=0)),
                ('hits_strong', models.IntegerField(default=0)),
                ('dmg_strong', models.IntegerField(default=0)),
                ('frags_strong', models.IntegerField(default=0)),
                ('acc_strong', models.DecimalField(max_digits=5, default=0, decimal_places=2)),
                ('shots_weak', models.IntegerField(default=0)),
                ('hits_weak', models.IntegerField(default=0)),
                ('dmg_weak', models.IntegerField(default=0)),
                ('frags_weak', models.IntegerField(default=0)),
                ('acc_weak', models.DecimalField(max_digits=5, default=0, decimal_places=2)),
                ('matchresult', models.ForeignKey(related_name='+', to='warmama.MatchResult')),
            ],
            options={
                'db_table': 'match_weapons',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('login', models.CharField(unique=True, max_length=64)),
                ('nickname', models.CharField(blank=True, max_length=64)),
                ('ip', models.CharField(blank=True, max_length=22)),
                ('ipv6', models.CharField(blank=True, max_length=54)),
                ('location', models.CharField(blank=True, db_index=True, max_length=2)),
                ('banned', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'players',
            },
        ),
        migrations.CreateModel(
            name='PlayerAchievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('achievement', models.ForeignKey(related_name='+', to='warmama.Achievement')),
                ('player', models.ForeignKey(related_name='achievements', to='warmama.Player')),
            ],
            options={
                'db_table': 'player_achievements',
            },
        ),
        migrations.CreateModel(
            name='PlayerSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('ip', models.CharField(blank=True, max_length=22)),
                ('ipv6', models.CharField(blank=True, max_length=54)),
                ('digest', models.CharField(default=uuid.uuid4, max_length=32)),
                ('ticket_id', models.IntegerField(null=True, blank=True, default=0)),
                ('ticket_expiration', models.DateTimeField(null=True, blank=True)),
                ('purgable', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'sessions_player',
            },
        ),
        migrations.CreateModel(
            name='PlayerStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('wins', models.IntegerField(default=0)),
                ('losses', models.IntegerField(default=0)),
                ('quits', models.IntegerField(default=0)),
                ('rating', models.DecimalField(max_digits=8, default=0, decimal_places=2)),
                ('deviation', models.DecimalField(max_digits=8, default=0, decimal_places=2)),
                ('gametype', models.ForeignKey(related_name='+', to='warmama.Gametype')),
                ('player', models.ForeignKey(related_name='stats', to='warmama.Player')),
            ],
            options={
                'db_table': 'player_stats',
            },
        ),
        migrations.CreateModel(
            name='PurgePlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('player', models.OneToOneField(to='warmama.Player', related_name='+')),
            ],
            options={
                'db_table': 'purge_players',
            },
        ),
        migrations.CreateModel(
            name='RaceRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('utctime', models.DateTimeField()),
                ('map', models.ForeignKey(related_name='+', to='warmama.Map')),
                ('player', models.ForeignKey(related_name='+', to='warmama.Player')),
            ],
            options={
                'db_table': 'race_runs',
            },
        ),
        migrations.CreateModel(
            name='RaceSector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('sector', models.IntegerField()),
                ('time', models.IntegerField(db_index=True, default=0)),
                ('run', models.ForeignKey(related_name='sectors', to='warmama.RaceRun')),
            ],
            options={
                'db_table': 'race_sectors',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('login', models.CharField(unique=True, max_length=64)),
                ('regip', models.CharField(blank=True, db_index=True, max_length=22)),
                ('regipv6', models.CharField(blank=True, max_length=54)),
                ('hostname', models.CharField(blank=True, max_length=64)),
                ('ip', models.CharField(blank=True, db_index=True, max_length=22)),
                ('ipv6', models.CharField(blank=True, max_length=54)),
                ('location', models.CharField(blank=True, db_index=True, max_length=2)),
                ('banned', models.BooleanField(default=False)),
                ('demos_baseurl', models.CharField(blank=True, max_length=128)),
            ],
            options={
                'db_table': 'servers',
            },
        ),
        migrations.CreateModel(
            name='ServerSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('ip', models.CharField(blank=True, db_index=True, max_length=22)),
                ('ipv6', models.CharField(blank=True, max_length=54)),
                ('digest', models.CharField(default=uuid.uuid4, max_length=36)),
                ('port', models.IntegerField()),
                ('next_match_uuid', models.CharField(blank=True, unique=True, max_length=36)),
                ('user', models.OneToOneField(to='warmama.Server', related_name='session')),
            ],
            options={
                'db_table': 'sessions_server',
            },
        ),
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=2)),
                ('fullname', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'weapons',
            },
        ),
        migrations.AddField(
            model_name='racerun',
            name='server',
            field=models.ForeignKey(related_name='+', to='warmama.Server'),
        ),
        migrations.AddField(
            model_name='purgeplayer',
            name='server_session',
            field=models.ForeignKey(blank=True, to='warmama.ServerSession', null=True, db_column='server_session', related_name='+', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='purgeplayer',
            name='session',
            field=models.OneToOneField(to='warmama.PlayerSession', related_name='purge_player'),
        ),
        migrations.AddField(
            model_name='playersession',
            name='server_session',
            field=models.ForeignKey(blank=True, to='warmama.ServerSession', null=True, db_column='server_session', related_name='+', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='playersession',
            name='ticket_server',
            field=models.ForeignKey(blank=True, to='warmama.ServerSession', null=True, db_column='ticket_server', related_name='+', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='playersession',
            name='user',
            field=models.OneToOneField(to='warmama.Player', related_name='session'),
        ),
        migrations.AddField(
            model_name='matchweapon',
            name='player',
            field=models.ForeignKey(related_name='+', to='warmama.Player'),
        ),
        migrations.AddField(
            model_name='matchweapon',
            name='weapon',
            field=models.ForeignKey(related_name='+', to='warmama.Weapon'),
        ),
        migrations.AddField(
            model_name='matchresult',
            name='server',
            field=models.ForeignKey(related_name='matches', to='warmama.Server'),
        ),
        migrations.AddField(
            model_name='matchresult',
            name='winner_player',
            field=models.ForeignKey(blank=True, to='warmama.MatchPlayer', null=True, related_name='+'),
        ),
        migrations.AddField(
            model_name='matchresult',
            name='winner_team',
            field=models.ForeignKey(blank=True, to='warmama.MatchTeam', null=True, related_name='+'),
        ),
        migrations.AddField(
            model_name='matchplayer',
            name='matchresult',
            field=models.ForeignKey(related_name='players', to='warmama.MatchResult'),
        ),
        migrations.AddField(
            model_name='matchplayer',
            name='matchteam',
            field=models.ForeignKey(blank=True, to='warmama.MatchTeam', null=True, related_name='players'),
        ),
        migrations.AddField(
            model_name='matchplayer',
            name='player',
            field=models.ForeignKey(related_name='matches', to='warmama.Player'),
        ),
        migrations.AddField(
            model_name='matchfrag',
            name='attacker',
            field=models.ForeignKey(related_name='+', to='warmama.Player'),
        ),
        migrations.AddField(
            model_name='matchfrag',
            name='matchresult',
            field=models.ForeignKey(related_name='frags', to='warmama.MatchResult'),
        ),
        migrations.AddField(
            model_name='matchfrag',
            name='victim',
            field=models.ForeignKey(related_name='+', to='warmama.Player'),
        ),
        migrations.AddField(
            model_name='matchfrag',
            name='weapon',
            field=models.ForeignKey(blank=True, to='warmama.Weapon', null=True),
        ),
        migrations.AddField(
            model_name='matchaward',
            name='matchresult',
            field=models.ForeignKey(related_name='+', to='warmama.MatchResult'),
        ),
        migrations.AddField(
            model_name='matchaward',
            name='player',
            field=models.ForeignKey(related_name='+', to='warmama.Player'),
        ),
        migrations.AlterUniqueTogether(
            name='racesector',
            unique_together=set([('run', 'sector')]),
        ),
        migrations.AlterUniqueTogether(
            name='playerstat',
            unique_together=set([('player', 'gametype')]),
        ),
        migrations.AlterUniqueTogether(
            name='matchteam',
            unique_together=set([('matchresult', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='matchplayer',
            unique_together=set([('player', 'matchresult')]),
        ),
    ]
