import argparse
from detect_card import detect_card

def main():
	parser = argparse.ArgumentParser(description='Card Detection')
	parser.add_argument('--image', help='image path')
	parser.add_argument('--directory', help='directory path')
	args = parser.parse_args()
	
	card_obj=detect_card(Image_Path=args.image,
		    Directory_Path=args.directory)
	card_obj.get_cards()


if __name__ == "__main__":
	main()