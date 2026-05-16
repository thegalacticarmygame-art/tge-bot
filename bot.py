import os
import json
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DATA_FILE = "claimed_keys.json"

MOFF_KEYS = [
    "MOFF-5577-TARKIN", "MOFF-2266-RULE", "MOFF-9988-SECTOR",
    "MOFF-1144-COMMAND", "MOFF-7733-GRAND", "MOFF-4488-OVERSEER",
    "MOFF-6655-WARDEN", "MOFF-3399-DECREE", "MOFF-8822-EDICT",
    "MOFF-5511-IRON", "MOFF-1188-PROVINCE", "MOFF-7722-DOMINION",
    "MOFF-4455-PROCLAIM", "MOFF-9966-MANDATE", "MOFF-2233-PRESIDE",
    "MOFF-8877-OUTPOST", "MOFF-3344-CITADEL", "MOFF-6611-FORTRESS",
    "MOFF-5599-CAPITAL", "MOFF-1133-CHANCELLOR", "MOFF-7755-VICEROY",
    "MOFF-4422-MAGISTRATE", "MOFF-9977-PROCONSUL", "MOFF-2299-PREFECT",
    "MOFF-8866-SATRAP", "MOFF-3322-REGENT", "MOFF-6677-DISCIPLINE",
    "MOFF-5544-PROCURATOR", "MOFF-1166-DESPOT", "MOFF-7799-IMPERIUM"
]

ROLE_KEYS = {
    1418878656104628234: [
        "OC-1001-CAPTAIN", "OC-2034-COMMANDER", "OC-3127-LIEUTENANT",
        "OC-4290-ADMIRAL", "OC-5183-COLONEL", "OC-6275-MAJOR",
        "OC-7368-GENERAL", "OC-8451-MARSHAL", "OC-9544-ENSIGN",
        "OC-1637-OFFICER", "OC-2730-COMMAND", "OC-3823-BRIDGE",
        "OC-4916-DECK", "OC-5009-RANK", "OC-6192-SALUTE",
        "OC-7285-DUTY", "OC-8378-HONOR", "OC-9461-RESOLVE",
        "OC-1554-VALOR", "OC-2647-IRON", "OC-3730-STEEL",
        "OC-4823-SHIELD", "OC-5916-OATH", "OC-6009-CADET",
        "OC-7192-BARON", "OC-8285-HELM", "OC-9378-FLAGSHIP",
        "OC-1471-CRUISER", "OC-2564-DESTROYER", "OC-3657-VANGUARD"
    ],

    1418881331919847504: [
        "ISB-9821-CRIMSON", "ISB-3344-AGENT", "ISB-7766-SPY",
        "ISB-2255-CIPHER", "ISB-8899-ASSET", "ISB-1199-WATCH",
        "ISB-4422-COVERT", "ISB-6677-PROBE", "ISB-5588-HUNT",
        "ISB-3311-FILE", "ISB-2244-DOSSIER", "ISB-7799-CODENAME",
        "ISB-5566-INFORMANT", "ISB-8811-INTERROGATE", "ISB-9933-SURVEIL",
        "ISB-4477-DEEPCOVER", "ISB-1155-PURGE", "ISB-6688-REDLIST",
        "ISB-3322-BLACKOPS", "ISB-7744-DETAIN", "ISB-2266-ARCHIVE",
        "ISB-9911-DECRYPT", "ISB-5533-SHADOW", "ISB-8855-OBSERVE",
        "ISB-4488-INFILTRATE", "ISB-1144-WHISPER", "ISB-6622-EAVESDROP",
        "ISB-3377-WIRETAP", "ISB-7755-TRACE", "ISB-2288-VERIFY"
    ],

    1418878334225354752: MOFF_KEYS,
    1418878371638804533: MOFF_KEYS
}

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"claimed": {}, "used_keys": []}

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"claimed": {}, "used_keys": []}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


@bot.tree.command(name="get-key", description="Claim your one-time key.")
async def get_key(interaction: discord.Interaction):
    data = load_data()
    user_id = str(interaction.user.id)

    if user_id in data["claimed"]:
        await interaction.response.send_message(
            f"You already claimed a key:\n`{data['claimed'][user_id]}`",
            ephemeral=True
        )
        return

    user_role_ids = [role.id for role in interaction.user.roles]

    matching_role_id = None
    for role_id in ROLE_KEYS:
        if role_id in user_role_ids:
            matching_role_id = role_id
            break

    if matching_role_id is None:
        await interaction.response.send_message(
            "You do not have the required role to claim a key.",
            ephemeral=True
        )
        return

    available_keys = [
        key for key in ROLE_KEYS[matching_role_id]
        if key not in data["used_keys"]
    ]

    if not available_keys:
        await interaction.response.send_message(
            "There are no keys left for your role.",
            ephemeral=True
        )
        return

    key = random.choice(available_keys)

    data["claimed"][user_id] = key
    data["used_keys"].append(key)
    save_data(data)

    await interaction.response.send_message(
        f"Here is your key:\n`{key}`",
        ephemeral=True
    )


bot.run(TOKEN)
