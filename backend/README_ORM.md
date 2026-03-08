# ORM

## CREATE
### 1
- from apps.music.models import Album
- album = Album(title='Солодка та гірка')
- album.save()

### 2
- from apps.music.models import Album
- i = Album.objects.create(title='123')

### 3
- from apps.music.models import Album
- album, created = Album.objects.get_or_create(title='1234')

### 4
- from apps.music.models import Album
- a1 = Album(title='12345')
- a2 = Album(title='12345666')
- Album.objects.bulk_create([a1, a2], batch_size=1000)

## READ
### single with error if not exists
- a = Album.objects.get(id=111163)
- a = Album.objects.get(title='123499')
- a = Album.objects.get(title='123499', id=111163)
- Album.objects.all()[:1][0]

### maybe single
- a = Album.objects.first()
- a = Album.objects.last()
### a few
- Album.objects.all()[2:5]
- Album.objects.all()
- albums_qs = Album.objects.all()
### filters
albums_qs = Album.objects.all()
>>> albums_qs = albums_qs.filter(id=55)
>  Album.objects.filter(id__in=[55, 66, 777])
> Album.objects.filter(id__gt=111000).count()
>  Album.objects.filter(id__gt=111000).exists()
> >>> data = Album.objects.filter(id__gt=1111000)
>>> n = 1 if data else 100
> data = Album.objects.filter(id__gt=1111, title="123499")
> data = Album.objects.filter(id__gt=1111, title__contains="12349")
data = data.filter(title__startswith='123495').filter(id__gt=50)
>  data.exclude(id=111159,)
> 
> 
> LEFT JOIN
> from apps.music.models import MusicComposition
> mc = MusicComposition.objects.select_related('album').last()
>  mc.album   # no N+1
> 
> 
> Reaction.objects.create(user_id=1, composition_id=3, title='Cool!!!')
> Reaction.objects.create(user_id=1, composition=mc, text='Cool222!!!')
> reaction = Reaction.objects.select_related('composition__album').last()

UPDATE DATA
 reaction
<Reaction: Reaction object (3)>
>>> reaction.text
'Cool222!!!'
>>> reaction.text = 'The best!!'
>>> reaction.save()
>>> reaction.text
'The best!!'
>>> reaction.text
'The best!!'
>>> reaction.refresh_from_db()
>>> reaction.text
'The best song I have ever heard!'
> 
> reactions = Reaction.objects.update(text='bla-bla')
> reactions = Reaction.objects.filter(id=3).update(text='bla-bla2')
> >>> reactions
1
> >>> reactions = Reaction.objects.filter(id__lte=3).update(text='bla-bla22')
>>> reactions = Reaction.objects.filter(id__in=[3, 8]).update(text='bla-bla2555552')
>>> reactions
1


DELETE
>>> reactions = Reaction.objects.filter(id=1).delete()
>>> reactions
(1, {'music.Reaction': 1})
> >>> reaction.delete()
(1, {'music.Reaction': 1})