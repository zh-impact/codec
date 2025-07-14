import os
import chardet
import click

@click.group()
@click.help_option('-h', '--help')
@click.pass_context
def cli(ctx):
    pass

@cli.command()
@click.help_option('-h', '--help')
@click.argument('filepath', type=click.Path(exists=True, dir_okay=False))
def detect(filepath):
    click.echo(f"Converting encoding for {filepath}")

    filename = os.path.basename(filepath)
    output_filepath = os.path.join('output', filename)

    with open(filepath, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    click.echo(result)

    try:
        text = raw_data.decode(result['encoding'])
        click.echo(f"Decoded with {result['encoding']} successfully")
    except UnicodeDecodeError as e:
        click.echo(f"Failed to decode file with {result['encoding']} encoding")
        print(f"UnicodeDecodeError: {e}")
        start = e.start
        end = min(start + 10, len(raw_data))
        print(f"\n Bytes around error (os {start} to {end}):")
        print(raw_data[start:end])
        # print(raw_data[start-10:start+10])
        print(f"Try decoding with GB18030 instead...")
        try:
            text = raw_data.decode('gb18030')
            click.echo(len(text))
            click.echo("Decoded with GB18030 successfully")
        except UnicodeDecodeError as e:
            text = "decode failed"
            click.echo(f"Decoding with GB18030 also failed. Please check the file.")
            print(f"UnicodeDecodeError: {e}")
    finally:
        click.echo("Writing to output file...")
        # click.echo(text)
        open(output_filepath, 'w', encoding='utf-8').write(text)
        click.echo("Done")

if __name__ == '__main__':
    cli()
