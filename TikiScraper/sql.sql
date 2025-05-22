CREATE TABLE IF NOT EXISTS "category"(
	"id"	INTEGER NOT NULL UNIQUE, -- id danh mục
	"name"	TEXT, -- tên danh mục
	"thumbnail_url"	TEXT, -- đường link tới ảnh thumbnail danh mục (có thể có hoặc không)
	"link"	TEXT, -- đường link xem các sản phẩm trong danh mục
	"product_count"	INTEGER, -- số lượng sản phẩm trong danh mục (có thể có hoặc không)
	"is_leaf"	INTEGER, -- 0 hoặc 1, đánh dấu danh mục có phải nút lá hay không (danh mục không thể chia nhỏ)
	"parent_id"	INTEGER, -- id danh mục cha
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "product" (
	"id"	INTEGER NOT NULL UNIQUE, -- id sản phẩm
	"name"	TEXT, -- tên sản phẩm
	"link"	TEXT, -- đường link dẫn tới sản phẩm
	"thumbnail_url"	TEXT, -- đường link thumbnail sản phẩm
	"direct_category"	INTEGER, -- danh mục trực tiếp nơi lấy dữ liệu sản phẩm
	"category_path"	TEXT, -- dạng chuỗi của mảng chứa các id danh mục theo thứ tự id trước là id cha của id sau, id cuối là danh mục chính của sản phẩm. Id cuối có thể khác so với direct_category (1 sản phẩm có thể có nhiều danh mục cuối/danh mục lá)
	"seller_id"	INTEGER, -- id của cửa hàng (chỉ dùng để lấy các dữ liệu khác)
	"seller_name" TEXT, -- tên cửa hàng
	"price"	REAL, -- giá hiện tại
	"original_price"	REAL, -- giá gốc
	"discount"	REAL, -- số tiền được giảm = giá gốc - giá hiện tại
	"discount_rate"	REAL, -- phần trăm tiền được discount
	"rating_average"	REAL, -- số sao trung bình
	"review_count"	INTEGER, -- số lượng review
	"inventory_status"	TEXT, -- trạng thái hiện tại của sản phẩm (có thể là available, notavailable, ...)
	"inventory_type"	TEXT, -- loại hình quản lý và cung cấp hàng hoá (có thể là instock, backorder, preorder, ...)
	"quantity_sold"	INTEGER, -- số lượng đã bán
	"description"	TEXT, -- mô tả (đã lọc html tags)
	"brand_name"	TEXT, -- tên thương hiệu
	"authors"	TEXT, -- tên các tác giả (nếu sản phẩm là sách, có thể có hoặc không)
	"specifications"	TEXT, -- các thông số kỹ thuật (dạng chuỗi của dictionary, đã lọc html tags)
	PRIMARY KEY("id"),
	CONSTRAINT "fk_category" FOREIGN KEY("direct_category") REFERENCES "category"("id") ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "review" (
	"id"	INTEGER NOT NULL UNIQUE, -- id review
	"product_id"	INTEGER, -- id sản phẩm
	"rating"	REAL, -- số sao
	"content"	TEXT, -- nội dung
	PRIMARY KEY ("id"),
	CONSTRAINT "fk_product" FOREIGN KEY("product_id") REFERENCES "product"("id") ON UPDATE RESTRICT ON DELETE RESTRICT
);