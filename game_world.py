world = {
    'entrance_hall': {
        'description': 'A grand entrance hall with towering bookshelves that scrape the high ceiling, their wood groaning under the weight of countless volumes. A large, ornate door, sealed with an unknown mechanism, dominates one wall. Dust motes dance in the lone shaft of light piercing the gloom, and the air carries a heavy scent of antiquity and decaying paper.',
        'exits': {'east': 'hall_of_scrolls'},
        'items': []
    },
    'hall_of_scrolls': {
        'description': 'A seemingly endless hall lined with shelves overflowing with scrolls of various sizes and ages. Thousands upon thousands of scrolls are crammed into every available space, some even appearing to float, slowly orbiting each other in strange, mesmerizing patterns. The air smells strongly of old parchment and a potent, almost palpable hint of magic.',
        'exits': {'west': 'entrance_hall', 'north': 'silent_study'},
        'items': ['strange_scroll']
    },
    'silent_study': {
        'description': 'An almost supernaturally quiet room, the silence broken only by the faint rustle of your own movements. Comfortable, albeit ancient, armchairs are arranged around old, polished wooden desks. The rich scent of old paper and aged leather fills the air, inviting contemplation.',
        'exits': {'south': 'hall_of_scrolls', 'north': 'chamber_of_riddles'},
        'items': ['dusty_tome']
    },
    'chamber_of_riddles': {
        'description': "A circular chamber with high, domed ceilings. Strange symbols cover the walls, pulsing faintly in the dim light, and a pedestal stands in the center. The air hums with a faint, almost inaudible energy.",
        'exits': {'south': 'silent_study'},
        'items': ['glowing_orb']
    }
}

items = {
    'strange_scroll': {
        'description': 'A peculiar scroll made of surprisingly resilient, aged parchment. It is covered in strange, intricate symbols that seem to shift when you are not looking directly at them. It hums with a faint energy and might contain a clue or a fragment of a map.'
    },
    'dusty_tome': {
        'description': 'An incredibly heavy, leather-bound book, its cover thick with a stubborn layer of grey dust. The cover itself is featureless, or perhaps any inscription has long since been worn away by time. It feels ancient to the touch.'
    },
    'glowing_orb': {
        'description': "A smooth, glass-like orb that emits a soft, pulsating light, casting gentle shadows on the walls. It feels pleasantly warm to the touch."
    }
}
